import { useParams } from "react-router-dom";
import { useEffect, useState, useRef, useMemo } from "react";
import { createHttpService } from "../../services/HTTPServices";
import getSocket from "../../services/WSServices";

import useFinishTurn from "../GameLogic/FinishTurnContainer.jsx";
import useDrawCard from "../GameLogic/DrawCardContainer.jsx";
import PlayerHandComponent from "../../components/PlayerHand/PlayerHandComponent";
import useSets from "../GameLogic/PlaySetContainer.jsx";
import useGameRoomData from "../Game/GameRoomContainer.jsx";
import useGameNotification from "../Game/GameNotificationsContainer.jsx";
import useTurnActions from "../../hooks/PlayerHand/useTurnActions.js";
import useSecretsFlow from "../../hooks/PlayerHand/useSecretsFlow.js";
import useAriadneFlow from "../../hooks/PlayerHand/useAriadneFlow.js";
import useStealSet from "../../hooks/PlayerHand/useStealSet.js";
import { useEventCardStore } from "../../Store/useEventCardStore.jsx";
import { useDeadCardFollyStore } from "../../Store/DeadCardFollyStore.jsx";
import { useAnotherVictimStore } from "../../Store/AnotherVictimStore.jsx";
import { usePointYourSuspicionsStore } from "../../Store/PointYourSuspicionsStore.jsx";

import SelectSecretCardModal from "../../components/Modals/SelectSecretCard.jsx";
import SelectPlayerModal from "../../components/Modals/SelectPlayer.jsx";
import SelectCardModal from "../../components/Modals/SelectCardModal.jsx";
import WaitingModal from "../../components/Modals/WaitingModal.jsx";
import OponentSets from "../../components/OponentSets/OponentSets.jsx";
import SelectPlayerToStealSetModal from "../../components/Modals/SelectPlayerForSets.jsx";
import SelectSetToStealModal from "../../components/Modals/SelectSetToStealModal.jsx";
import SelectDirectionModal from "../../components/Modals/SelectDirectionModal.jsx";

export default function PlayerHandContainer({
  playerId,
  setDiscardedCount,
  selectedDraftCards,
  setSelectedDraftCards,
  selectedDrawCardsNumber,
  setSelectedDrawCardsNumber,
  playersNumber,
}) {
  //SECTION - INIT: hooks, services and shared data
  // - Hooks that bring global/game scoped data
  // - Services and refs used across the container
  const { gameId } = useParams();
  const {
    allSets,
    requestedPlayerSets,
    selectRequest,
    fetchPlayerSets,
    playSet,
    isLoadingSets,
    error,
  } = useSets(gameId, playerId);
  const { jugadores: players, actualTurn, inCourse } = useGameRoomData(gameId);
  const {
    emitWaitingModals,
    secretNotification,
    emitSecretResolved,
    selectSecretRequest,
    ariadneNotification,
  } = useGameNotification(gameId);

  // Sockets / services / refs
  const socketRef = useRef(null);
  const [httpService] = useState(() => createHttpService());
  const {
    finish: finishTurn,
    loading: finishLoading,
    error: finishError,
  } = useFinishTurn();
  const drawCard = useDrawCard();
  // Ref used to store transient action context (prevents race conditions)
  // (moved into useSecretsFlow hook)

  //!SECTION - INIT

  //SECTION - STATE: UI, turn & gameplay related state grouped by responsibility
  // - UI / player hand
  // - Turn state and derived helpers
  // - Modals / set/secret/ariadne state
  // - Steal-set state (below, kept near handlers)
  // UI state
  const [loading, setLoading] = useState(true);
  const [playerHand, setPlayerHand] = useState([]);
  const [selectedCards, setSelectedCards] = useState([]);
  // Turn logic (currentTurnIndex/myPlayerIndex kept here; actions delegated to hook)
  const [currentTurnIndex, setCurrentTurnIndex] = useState(null);
  const [myPlayerIndex, setMyPlayerTurnNumber] = useState(null);
  // Derived helper
  const isMyTurn = useMemo(() => {
    return (
      currentTurnIndex != null &&
      myPlayerIndex != null &&
      currentTurnIndex === myPlayerIndex
    );
  }, [currentTurnIndex, myPlayerIndex]);

  // Modals / set & secret flow state
  const [isSelectPlayerOpen, setIsSelectPlayerOpen] = useState(false);
  const [targetPlayerName, setTargetPlayerName] = useState("");
  const [playedSet, setPlayedSet] = useState(null);
  const [ariadneCardId, setAriadneCardId] = useState();
  const [hasPlayedSet, setHasPlayedSet] = useState();

  // Event Cards
  const { selectPlayer, eventCardClicked } = useEventCardStore.getState();
  const selectCard = useDeadCardFollyStore((state) => state.selectCard);
  const selectDirection = useDeadCardFollyStore(
    (state) => state.selectDirection
  );
  const {
    setTargetPlayerToStealSet,
    setselectPlayerToStealSet,
    setSelectSetToStealOpen,
  } = useAnotherVictimStore.getState();
  const selectPlayerToStealSet = useAnotherVictimStore(
    (state) => state.selectPlayerToStealSet
  );
  const targetPlayerToStealSet = useAnotherVictimStore(
    (state) => state.targetPlayerToStealSet
  );
  const selectSetToStealOpen = useAnotherVictimStore(
    (state) => state.selectSetToStealOpen
  );
  const newStolenSet = useAnotherVictimStore((state) => state.newStolenSet);

  const selectPlayerSuspicions = usePointYourSuspicionsStore(
    (state) => state.selectPlayerSuspicions
  );

  // Secret Revealing by Event
  const votedToReveal = useEventCardStore((state) => state.votedToReveal);
  const votedPlayerId = useEventCardStore((state) => state.votedPlayerId);
  const secretsByPlayer = useEventCardStore((state) => state.secretsByPlayer);
  const { setVotedToReveal } = useEventCardStore.getState();

  // ==================================================
  // TURN HOOK: extract turn-related handlers & flags
  // ==================================================
  const {
    handlePlayEventClick,
    handleDiscardCard,
    handleDrawCardClick,
    handleFinishClick,
    handleCardClick,
    isDiscardDisabled,
    isFinishDisabled,
    isDrawDisable,
    secondsLeft,
    onEventCardClick,
  } = useTurnActions({
    gameId,
    playerId,
    playerHand,
    selectedCards,
    setSelectedCards,
    selectedDraftCards,
    setSelectedDraftCards,
    selectedDrawCardsNumber,
    setSelectedDrawCardsNumber,
    httpService,
    drawCard,
    finishTurn,
    isMyTurn,
    finishLoading,
    setDiscardedCount,
    hasPlayedSet,
    setHasPlayedSet,
    playersNumber,
  });

  //!SECTION - TURN HOOK

  //SECTION - ARIADNE HOOK
  // Inputs: { gameId, playerId, fetchPlayerSets, httpService }
  // Outputs: { ariadneContext, handleAriadne, handlePlayAriadne }
  // Responsibility: store Ariadne card context, request target player's sets and play Ariadne against a chosen set
  const {
    ariadneContext: ariadneHookContext,
    handleAriadne: handleAriadneHook,
    handlePlayAriadne,
  } = useAriadneFlow({
    gameId,
    playerId,
    fetchPlayerSets,
    httpService,
  });
  //!SECTION - ARIADNE HOOK

  //SECTION - SECRETS HOOK
  // Inputs: { gameId, playerId, httpService, emitWaitingModals, emitSecretResolved, selectSecretRequest, secretNotification }
  // Outputs: { pendingSecrets, isSelectSecretOpen, setIsSelectSecretOpen, isWaitingModalOpen, setIsWaitingModalOpen,
  //            secretsOwnerId, secretEffect, openForActor, openForHide, revealByTargetInitiated, resolveSecret, currentActionRef }
  // Responsibility: manage secret selection modal lifecycle, socket subscription for secrets and resolution (update + optional steal)
  const {
    pendingSecrets,
    isSelectSecretOpen,
    setIsSelectSecretOpen,
    isWaitingModalOpen,
    setIsWaitingModalOpen,
    secretsOwnerId,
    secretEffect,
    setSecretEffect,
    openForActor,
    openForHide,
    revealByTargetInitiated,
    resolveSecret,
    currentActionRef,
  } = useSecretsFlow({
    gameId,
    playerId,
    httpService,
    emitWaitingModals,
    emitSecretResolved,
    selectSecretRequest,
    secretNotification,
  });
  //!SECTION - SECRETS HOOK

  //!SECTION - STATE

  //!SECTION - USE EFFECTS
  // NOTE: selectSecretRequest is handled inside `useSecretsFlow` hook

  useEffect(() => {
    if (!gameId || !playerId) return;

    let mounted = true;
    let onConnectNamed = null;

    const connectSocket = async () => {
      try {
        const sock = await getSocket();
        if (!socketRef.current) socketRef.current = sock;

        sock.on("game_info", handleGameInfo);
        sock.on("initial_hand", handleHandPayload);
        sock.on("player_hand", handleHandPayload);

        onConnectNamed = () => {
          sock.emit("get_hand", gameId, playerId);
          sock.emit("get_game_info", gameId, (ack) => {
            if (ack) handleGameInfo(ack);
          });
        };

        if (sock.connected) onConnectNamed();
        sock.on("connect", onConnectNamed);

        if (mounted) setLoading(false);
      } catch (err) {
        console.error("Socket connection failed:", err);
        if (mounted) setLoading(false);
      }
    };

    connectSocket();

    return () => {
      mounted = false;
      const sock = socketRef.current;
      if (sock) {
        sock.off("game_info", handleGameInfo);
        sock.off("initial_hand", handleHandPayload);
        sock.off("player_hand", handleHandPayload);
        if (onConnectNamed) sock.off("connect", onConnectNamed);
      }
    };
  }, [gameId, playerId]);

  //SECTION - SOCKET EVENT HANDLERS
  // Responsibility: handle incoming socket events (hand, game info, set play)
  // Keep these pure and only update local state or refs
  const handleHandPayload = (payload) => {
    if (Array.isArray(payload)) {
      const player_hand = payload.find(
        (p) => String(p.player_id) === String(playerId)
      );
      if (player_hand?.cards_list) setPlayerHand(player_hand.cards_list);
    } else if (payload && String(payload.player_id) === String(playerId)) {
      if (payload.cards_list) setPlayerHand(payload.cards_list);
    }
  };

  const handleGameInfo = (payload) => {
    if (!payload || typeof payload !== "object") return;
    if (payload.currentTurn !== undefined)
      setCurrentTurnIndex(payload.currentTurn);
    if (Array.isArray(payload.players)) {
      const me = payload.players.find(
        (p) => String(p.player_id) === String(playerId)
      );
      if (me) setMyPlayerTurnNumber(me.playerTurn);
    }
  };

  //SECTION - SETS: Play set flow
  // - Ttrigger server playSet
  // - Open player selection modal when server asks for a target
  const handlePlaySetClick = async () => {
    if (selectedCards.length === 0) return;
    try {
      const selectedIds = selectedCards.map((c) => c.id);
      const setResponse = await playSet(selectedIds);
      // Clear selected cards immediately after playing the set so the UI
      // no longer shows the just-played selection and prevents replaying.
      setSelectedCards([]);
      setIsSelectPlayerOpen(true);
      if (setResponse.message !== null) {
        setPlayedSet(setResponse.message);
      } else {
        // Ariadne set played
        setPlayedSet({ effect: "Ariadne Oliver" });
      }

      setHasPlayedSet(true);
    } catch (err) {
      console.error("Error al jugar el set:", err);
    }
  };

  useEffect(() => {
    if (!newStolenSet) return;

    if (newStolenSet?.result) {
      console.log(
        "PlayerHandContainer: new stolen set received:",
        newStolenSet
      );
    }
    setIsSelectPlayerOpen(true);
    setPlayedSet(newStolenSet.result);
    setHasPlayedSet(true);
  }, [newStolenSet]);
  //!SECTION - SETS

  //SECTION - ARIADNE NOTIFICATIONS
  // WE PLAY AN ARIADNE OLIVER CARD (Listener)
  useEffect(() => {
    if (ariadneNotification) {
      // we played this card
      if (ariadneNotification.owner_id === playerId) {
        console.log("AriadneNotification:", ariadneNotification);
        console.log(playedSet);
        setAriadneCardId(ariadneNotification.card_ids[0]);
        setIsSelectPlayerOpen(true);
      }
    }
  }, [ariadneNotification, playerId, playedSet]);

  //SECTION - WAITING MODAL: set target name when we receive a secret selection notification
  useEffect(() => {
    if (
      secretNotification?.type === "secret_selection_modal" &&
      String(secretNotification.target_player_id) === String(playerId)
    ) {
      const requester = (players || []).find(
        (p) =>
          String(p.id_jugador) === String(secretNotification.requester_id) ||
          String(p.player_id) === String(secretNotification.requester_id)
      );
      const requesterName = requester?.nombre || requester?.name || "Jugador";
      setTargetPlayerName(requesterName);
    }
  }, [secretNotification, playerId, players]);

  //!SECTION - ARIADNE NOTIFICATIONS

  //SECTION - STEAL-SET (moved to hook)
  // Responsibility: choose a player, load their sets and steal one
  const {
    targetPlayerSets,
    loadingTargetSets,
    handleSelectStealTarget,
    handleSelectSetToSteal,
  } = useStealSet({
    gameId,
    playerId,
    fetchPlayerSets,
    requestedPlayerSets,
    isLoadingSets,
    httpService,
    isMyTurn,
  });
  //!SECTION - STEAL-SET

  useEffect(() => {
    if (!socketRef.current) return;

    const sock = socketRef.current;

    const onAllSets = (payload) => {
      console.log("Sets actualizados en tiempo real:", payload);
    };
    sock.on("emit_all_sets", onAllSets);

    return () => {
      sock.off("emit_all_sets", onAllSets);
    };
  }, [socketRef]);
  //!SECTION
  //SECTION - RENDER: main component + modals
  // - PlayerHandComponent is the presentational part
  // - Below: conditional modal components for flows (sets, secrets, ariadne, steal)
  // ==================================================
  return (
    <>
      <PlayerHandComponent
        loading={loading}
        playerHand={playerHand}
        selectedCards={selectedCards}
        isDiscardDisabled={isDiscardDisabled}
        isFinishDisabled={isFinishDisabled}
        finishLoading={finishLoading}
        finishError={finishError}
        onDiscardCard={handleDiscardCard}
        onFinishClick={handleFinishClick}
        onCardClick={handleCardClick}
        onDrawClick={handleDrawCardClick}
        onPlaySetClick={handlePlaySetClick}
        isDrawDisable={isDrawDisable}
        secondsLeft={secondsLeft}
        isMyTurn={isMyTurn}
        onEventCardClick={onEventCardClick}
        onPlayEventClick={handlePlayEventClick}
      />
      {/* Select Card (Event Card) */}
      {selectCard && (
        <SelectCardModal
          cards={playerHand}
          players={players}
          playerId={playerId}
          gameId={gameId}
          eventSelectedCard={selectedCards}
        />
      )}
      {/* Select Direction (Event Card) */}
      {selectDirection && <SelectDirectionModal />}
      {/* Select Player (Event Card) */}
      {(selectPlayer || selectPlayerSuspicions) && (
        <SelectPlayerModal
          players={players}
          playerId={playerId}
          effect={
            selectPlayerSuspicions
              ? "Point Your Suspicions"
              : eventCardClicked?.effect
          }
        />
      )}

      {/* Event Card - Devious */}
      {votedToReveal &&
        votedPlayerId === playerId &&
        secretsByPlayer[playerId] && (
          <SelectSecretCardModal
            effect="REVEAL"
            secrets={secretsByPlayer[playerId].secrets_list}
            isOwner={true}
            onConfirm={async (secretId) => {
              await httpService.updateSecret(gameId, {
                player_id: playerId,
                secret_id: secretId,
                effect: "REVEAL",
              });
              setVotedToReveal(false);
            }}
          />
        )}
      {isSelectPlayerOpen && playedSet && (
        <SelectPlayerModal
          players={players}
          playerId={playerId}
          effect={playedSet.effect}
          onConfirm={async (player) => {
            setTargetPlayerName(player.name);
            setIsSelectPlayerOpen(false);

            if (
              playedSet.effect === "Reveal by Target" ||
              playedSet.effect === "Steal"
            ) {
              await revealByTargetInitiated(playedSet.id, player.id);
            } else if (playedSet.effect === "Reveal by Actor") {
              openForActor(player.id, "REVEAL");
            } else if (playedSet.effect === "Hide") {
              openForHide(player.id, "HIDE");
            } else if (playedSet.effect === "Ariadne Oliver") {
              // pass stored card id to hook when starting the Ariadne flow
              console.log("PlayerHandContainer: starting Ariadne flow ->", {
                player,
                ariadneCardId,
                playedSet,
              });
              setSecretEffect("REVEAL");
              setTargetPlayerName(player.name);
              handleAriadneHook(player, ariadneCardId);
            }
          }}
        />
      )}
      {selectPlayerToStealSet && (
        <SelectPlayerToStealSetModal
          players={players}
          playerId={playerId}
          onConfirm={handleSelectStealTarget}
          onCancel={() => setselectPlayerToStealSet(false)}
        />
      )}
      {selectSetToStealOpen && targetPlayerToStealSet && (
        <SelectSetToStealModal
          sets={targetPlayerSets}
          playerName={
            targetPlayerToStealSet.nombre || targetPlayerToStealSet.name || ""
          }
          loading={loadingTargetSets || isLoadingSets}
          onConfirm={handleSelectSetToSteal}
          onCancel={() => {
            setSelectSetToStealOpen(false);
          }}
        />
      )}
      {isSelectSecretOpen && pendingSecrets && (
        <SelectSecretCardModal
          effect={currentActionRef.current.effect}
          secrets={pendingSecrets}
          isOwner={playerId === secretsOwnerId}
          onConfirm={async (secretId) => {
            await resolveSecret(secretId);
          }}
        />
      )}
      {ariadneHookContext && (
        <OponentSets
          jugador={ariadneHookContext.jugador}
          playerId={playerId}
          onSelectSet={async (set) => {
            await handlePlayAriadne(set);

            // show waiting modal and clear local stored card id
            setIsWaitingModalOpen(true);
            setAriadneCardId(null);
          }}
        />
      )}
      {isWaitingModalOpen && (
        <WaitingModal targetName={targetPlayerName} effect={secretEffect} />
      )}
    </>
  );
}
