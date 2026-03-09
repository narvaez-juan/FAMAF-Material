import { useEffect, useRef, useState } from "react";
import { usePointYourSuspicionsStore } from "../../Store/PointYourSuspicionsStore";
import { useEventCardStore } from "../../Store/useEventCardStore";
import getSocket from "../../services/WSServices";

export default function useSecretsFlow({
  gameId,
  playerId,
  httpService,
  emitWaitingModals,
  emitSecretResolved,
  selectSecretRequest,
  secretNotification,
}) {
  const [pendingSecrets, setPendingSecrets] = useState([]);
  const [isSelectSecretOpen, setIsSelectSecretOpen] = useState(false);
  const [isWaitingModalOpen, setIsWaitingModalOpen] = useState(false);
  const [secretsOwnerId, setSecretsOwnerId] = useState(null);
  const [secretEffect, setSecretEffect] = useState(null);
  const votedToReveal = useEventCardStore((state) => state.votedToReveal);
  const votedPlayerId = useEventCardStore((state) => state.votedPlayerId);

  const currentActionRef = useRef(null);
  const socketRef = useRef(null);

  // React to incoming selectSecretRequest (from backend via HTTP flow)
  useEffect(() => {
    if (!selectSecretRequest) return;
    if (selectSecretRequest.target_player_id === playerId) {
      // We are the target and must reveal
      currentActionRef.current = {
        type: "REVEAL_BY_TARGET",
        requesterId: selectSecretRequest.requester_id,
        targetId: playerId,
        secretsOwnerId: playerId,
        effect: selectSecretRequest.effect,
        steal: selectSecretRequest.steal,
      };

      setSecretsOwnerId(playerId);
      setSecretEffect(selectSecretRequest.effect);
      setIsSelectSecretOpen(true);
    }
  }, [selectSecretRequest, playerId]);

  // React to notifications coming from socket/notifications for waiting modal and reveal
  useEffect(() => {
    if (!secretNotification) return;

    if (
      secretNotification.type === "secret_selection_modal" &&
      secretNotification.target_player_id === playerId
    ) {
      setSecretEffect(secretNotification.secret_effect);
      setIsWaitingModalOpen(true);
    }

    if (
      secretNotification.type === "secret_reveal_modal" &&
      secretNotification.target_player_id === playerId
    ) {
      setIsWaitingModalOpen(false);
    }
  }, [secretNotification, playerId]);

  // When select secret modal is open, ensure socket subscription to fetch secrets for owner
  useEffect(() => {
    if (!isSelectSecretOpen || !secretsOwnerId) return;

    let mounted = true;

    const connect = async () => {
      try {
        if (!localStorage.getItem("RoomID") && gameId) {
          localStorage.setItem("RoomID", gameId);
        }

        const sock = await getSocket();
        socketRef.current = sock;

        sock.emit("get_secrets", gameId, secretsOwnerId);

        const onConnect = () => {
          sock.emit("get_secrets", gameId, secretsOwnerId);
        };

        sock.on("connect", onConnect);
        sock.on("player_secrets", handleSecretPayload);

        if (mounted) {
          /* noop */
        }
      } catch (err) {
        console.error("Socket connection failed:", err);
      }
    };

    connect();

    return () => {
      mounted = false;
      const sock = socketRef.current;
      if (sock) {
        sock.off("player_secrets", handleSecretPayload);
      }
    };
  }, [
    isSelectSecretOpen,
    secretsOwnerId,
    gameId,
    votedToReveal,
    votedPlayerId,
  ]);

  const handleSecretPayload = (payload) => {
    try {
      if (payload.player_id === secretsOwnerId) {
        setPendingSecrets(payload.secrets_list);
      }
    } catch (error) {
      console.error("Error handling player_secrets payload:", error);
    }
  };

  // Called when the actor wants to reveal target's secret (actor flow)
  const openForActor = (targetPlayerId, effect = "REVEAL") => {
    currentActionRef.current = {
      type: "REVEAL_BY_ACTOR",
      requesterId: playerId,
      targetId: targetPlayerId,
      secretsOwnerId: targetPlayerId,
      effect,
    };

    setSecretEffect(effect);
    setSecretsOwnerId(targetPlayerId);
    if (emitWaitingModals) emitWaitingModals(playerId, targetPlayerId, effect);
    setIsSelectSecretOpen(true);
  };

  // Called when the actor wants to hide a secret
  const openForHide = (targetPlayerId, effect = "HIDE") => {
    const emitWaiting = playerId !== targetPlayerId;

    currentActionRef.current = {
      type: "HIDE",
      requesterId: playerId,
      targetId: targetPlayerId,
      secretsOwnerId: targetPlayerId,
      effect,
    };

    setSecretEffect(effect);
    setSecretsOwnerId(targetPlayerId);
    if (emitWaiting && emitWaitingModals)
      emitWaitingModals(playerId, targetPlayerId, effect);
    setIsSelectSecretOpen(true);
  };

  // Called when a set play requests the target to reveal (initiated flow)
  const revealByTargetInitiated = async (playedSetId, targetId) => {
    // Call server to process set then set waiting state
    try {
      await httpService.processSet(gameId, {
        set_id: playedSetId,
        target_player_id: targetId,
      });

      currentActionRef.current = {
        type: "REVEAL_BY_TARGET_INITIATED",
        requesterId: playerId,
        targetId,
        secretsOwnerId: targetId,
        effect: "REVEAL",
      };

      setSecretEffect("REVEAL");
      setIsWaitingModalOpen(true);
      setIsSelectSecretOpen(false);
    } catch (err) {
      console.error("Error processing set for reveal:", err);
      throw err;
    }
  };

  const resolveSecret = async (secretId) => {
    const context = currentActionRef.current;
    if (!context) {
      console.error("No action context available when resolving secret");
      return;
    }

    // Determine emitter/target for notification
    let emitPlayerId, emitTargetId;
    if (context.type === "REVEAL_BY_TARGET") {
      emitPlayerId = context.targetId;
      emitTargetId = context.requesterId;
    } else {
      emitPlayerId = context.requesterId;
      emitTargetId = context.targetId;
    }

    if (emitSecretResolved) emitSecretResolved(emitPlayerId, emitTargetId);

    try {
      await httpService.updateSecret(gameId, {
        player_id: context.secretsOwnerId,
        secret_id: secretId,
        effect: context.effect,
      });

      if (context.steal) {
        await httpService.stealSecret(gameId, {
          playerId: context.requesterId,
          targetPlayerId: context.targetId,
          secretId,
        });
      }
    } catch (err) {
      console.error("Error resolving secret:", err);
      throw err;
    } finally {
      currentActionRef.current = null;
      setSecretsOwnerId(null);
      setIsSelectSecretOpen(false);
      setPendingSecrets([]);
    }
  };

  return {
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
  };
}
