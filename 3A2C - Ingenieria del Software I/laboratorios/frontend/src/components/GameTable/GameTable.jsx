import PlayerInfo from "../PlayerInfo/PlayerInfo";
import Decks from "../Decks/Decks";
import PlayerSecret from "../PlayerSecrets/PlayerSecrets";
import PlayerSets from "../PlayerSets/PlayerSets";
import DraftPileContainer from "../../containers/DraftPile/DraftPileContainer";
import { toast, Toaster } from "react-hot-toast";
import { useState, useEffect } from "react";
import initWebSocketEventManager from "../../websocket/WebSocketEventManager";
import { handleGameEvent } from "../../websocket/handlers/WebSocketEventHandler";

export default function GameTable({
  jugadores,
  turnoActual,
  discardPile,
  drawPile,
  playerId,
  gameId,
  PlayerHandContainer,
  allSets,
}) {
  const [isDataLoaded, setIsDataLoaded] = useState(false);

  // Gestion de turnos
  const [selectedDraftCards, setSelectedDraftCards] = useState([]);
  const [selectedDrawCardsNumber, setSelectedDrawCardsNumber] = useState(0);
  const [discardedCount, setDiscardedCount] = useState(0);
  const [currentTurnIndex, setCurrentTurnIndex] = useState(-1);
  const totalSelected = selectedDraftCards.length + selectedDrawCardsNumber;

  // Gestion de notificaciones de evento
  const { eventPayload, actionEventPayload } = initWebSocketEventManager(gameId, playerId);

  useEffect(() => {
    if (eventPayload) {
      handleGameEvent(eventPayload, playerId, jugadores);
    }
  }, [eventPayload]);

  useEffect(() => {
    if (!actionEventPayload) return;

    const { actor_id, description } = actionEventPayload;

    if (String(actor_id) !== String(playerId)) {
      toast(description, { icon: "🃏" });
}
  }, [actionEventPayload, playerId]);

  const resolvePlayerId = (player) => {
    if (!player) return null;
    const rawId =
      player.id_jugador ??
      player.player_id ??
      player.playerId ??
      player.id ??
      null;
    return rawId != null ? String(rawId) : null;
  };

  const resolvePlayerTurnPosition = (player) => {
    if (!player) return null;
    return (
      player.posicionTurno ??
      player.turn_position ??
      player.turnPosition ??
      player.playerTurn ??
      null
    );
  };

  useEffect(() => {
    console.log("turnoActual now:", turnoActual);

    if (!jugadores.length || !turnoActual) {
      setCurrentTurnIndex(-1);
      return;
    }

    const currentTurnPlayerId = resolvePlayerId(turnoActual);
    const currentTurnPosition = resolvePlayerTurnPosition(turnoActual);

    let index = -1;

    if (currentTurnPlayerId != null) {
      index = jugadores.findIndex((j) => {
        const candidateId = resolvePlayerId(j);
        return candidateId != null && candidateId === currentTurnPlayerId;
      });
    }

    if (index === -1 && currentTurnPosition != null) {
      index = jugadores.findIndex((j) => {
        const candidatePos = resolvePlayerTurnPosition(j);
        return candidatePos != null && candidatePos === currentTurnPosition;
      });
    }

    setCurrentTurnIndex(index);
  }, [jugadores, turnoActual]);

  const siguienteTurno =
    currentTurnIndex >= 0 && jugadores.length > 0
      ? jugadores[(currentTurnIndex + 1) % jugadores.length]
      : null;

  const handleDrawPileRightClick = () => {
    setSelectedDrawCardsNumber((prev) => (prev > 0 ? prev - 1 : 0));
  };
  const handleDrawPileLeftClick = () => {
    setSelectedDrawCardsNumber((prev) => prev + 1);
  };

  useEffect(() => {
    // We consider the data loaded once `allSets` is an array, even if empty.
    // This signifies the initial fetch has completed.
    if (Array.isArray(allSets)) {
      setIsDataLoaded(true);
    }
  }, [allSets]);

  if (!isDataLoaded) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-slate-800">
        <p className="text-white text-xl font-metamorphous">Loading Sets...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen w-full">
      {/* Zona superior: jugadores + próximo turno */}
      <div className="flex flex-row w-full mb-12 gap-8 items-start px-6 pt-8">
        {/* Cajas de jugadores */}
        <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 relative gap-4">
          {jugadores.map((jugador, index) => {
            const jugadorId = resolvePlayerId(jugador);
            const isCurrentTurn = currentTurnIndex === index;
            const setsDelJugador =
              allSets.find((s) => {
                if (jugadorId == null) return false;
                const normalizedSetOwnerId =
                  s?.player_id != null ? String(s.player_id) : null;
                return normalizedSetOwnerId === jugadorId;
              })?.sets || [];

            const key = jugadorId ?? `player-${index}`;

            return (
              <div key={key} className="relative">
                <PlayerInfo
                  jugador={jugador}
                  esTurnoActual={isCurrentTurn}
                  playerId={playerId}
                />
                <div className="absolute mt-2 w-full flex justify-center z-10">
                  {setsDelJugador.length > 0 && (
                    <PlayerSets sets={setsDelJugador} />
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Próximo turno */}
        <div className="w-56 bg-slate-900 p-2 rounded-lg border border-slate-700 text-center shadow-[0_0_4px_#c2a22d]">
          <h3 className="p-1 text-base font-semibold mb-2 text-slate-200 font-metamorphous">
            Next turn
          </h3>
          {siguienteTurno ? (
            <p className="text-white text-base font-metamorphous">
              {siguienteTurno.nombre.length > 20
                ? siguienteTurno.nombre.slice(0, 17) + "..."
                : siguienteTurno.nombre}
            </p>
          ) : (
            <p className="text-slate-400">Not available</p>
          )}
        </div>
      </div>

      {/* Zona central - tablero */}
      <div className="flex flex-col items-center justify-center w-full gap-8 px-4 pb-8 flex-1">
        {/* Decks on top row */}
        <div className="w-full flex justify-center gap-8">
          <Decks
            drawPileCount={drawPile}
            drawPilePickCount={selectedDrawCardsNumber}
            discardPile={discardPile}
            setDrawPileLeftClicks={handleDrawPileLeftClick}
            setDrawPileRightClicks={handleDrawPileRightClick}
            totalSelected={totalSelected}
            discardedCount={discardedCount}
          />
          <DraftPileContainer
            gameId={gameId}
            playerId={playerId}
            onSelectDraftCards={setSelectedDraftCards}
            totalSelected={totalSelected}
            discardedCount={discardedCount}
          />
        </div>
      </div>

      <div className="relative w-full flex-1">
        {/* PlayerHand al fondo, encima de PlayerSets */}
        <div className="absolute bottom-0 left-0 w-full flex justify-center z-10">
          <Toaster
            position="bottom-right"
            containerStyle={{
              bottom: "430px",
              right: "22px",
              position: "fixed",
            }}
            toastOptions={{
              duration: 6000,
              style: {
                background: "#0b3b6f",
                color: "#fff",
                border: "1px solid #c2a22d",
                fontFamily: "Metamorphous",
                fontSize: "14px",
                maxWidth: "226px",
              },
            }}
          />
          <PlayerHandContainer
            playerId={playerId}
            setDiscardedCount={setDiscardedCount}
            selectedDraftCards={selectedDraftCards}
            setSelectedDraftCards={setSelectedDraftCards}
            selectedDrawCardsNumber={selectedDrawCardsNumber}
            setSelectedDrawCardsNumber={setSelectedDrawCardsNumber}
            playersNumber={jugadores.length}
          />
        </div>

        <PlayerSecret playerId={playerId} />
      </div>
    </div>
  );
}
