import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import useSets from "../../containers/GameLogic/PlaySetContainer";
import Card from "../Card/Card";

export default function OponentSets({ jugador, playerId, onSelectSet }) {
  if (!jugador) return null;

  const { gameId } = useParams();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { requestedPlayerSets = [], fetchPlayerSets } = useSets(
    gameId,
    playerId
  );

  const isInteractive = typeof onSelectSet === "function";
  const resolvePlayerId = (player) => {
    if (!player) return null;
    return (
      player.id_jugador ??
      player.player_id ??
      player.playerId ??
      player.id ??
      null
    );
  };
  const playerDisplayName = jugador.nombre || jugador.name || "Unknown";
  const resolvedId = resolvePlayerId(jugador);
  const targetPlayerId =
    resolvedId != null && !Number.isNaN(Number(resolvedId))
      ? Number(resolvedId)
      : null;

  const handleClick = async () => {
    setIsModalOpen(true);
    console.log(
      "OponentSets.handleClick: opening modal and fetching sets for",
      jugador
    );
    if (targetPlayerId == null) {
      console.warn("OponentSets: unable to resolve player id", jugador);
      return;
    }
    fetchPlayerSets(targetPlayerId);
  };

  useEffect(() => {
    if (isInteractive && targetPlayerId != null) {
      console.log(
        "OponentSets.useEffect: interactive mode, opening modal for",
        jugador
      );
      setIsModalOpen(true);
      fetchPlayerSets(targetPlayerId);
    }
  }, [isInteractive, targetPlayerId, fetchPlayerSets, jugador]);

  return (
    <>
      {/* Botón para ver sets del oponente */}
      {!isInteractive && (
        <button
          onClick={handleClick}
          className="w-full mt-2 px-3 py-1.5 rounded-lg text-sm font-metamorphous font-semibold transition-all duration-200 border border-yellow-600/50 hover:border-yellow-400 shadow-[0_0_4px_rgba(194,162,45,0.3)] hover:shadow-[0_0_8px_rgba(194,162,45,0.6)]"
          style={{ background: "#0b3b6f", color: "white" }}
          onMouseOver={(e) => {
            e.currentTarget.style.background = "#c2a22d";
            e.currentTarget.style.color = "black";
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.background = "#0b3b6f";
            e.currentTarget.style.color = "white";
          }}
        >
          See Sets
        </button>
      )}

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex flex-col">
          {/* Header */}
          <div
            className="bg-gradient-to-r from-blue-900/80 to-black/80 px-8 py-6 border-b border-yellow-400 
          flex items-center justify-between"
          >
            <div className="flex items-center gap-4">
              <div
                className="w-12 h-12 rounded-md bg-gradient-to-br from-[#112b57] to-[#0b3b6f] 
              flex items-center justify-center shadow-[0_0_4px_#c2a22d]"
              >
                <span className="text-3xl font-metamorphous font-bold text-[#c2a22d]">
                  {playerDisplayName.charAt(0).toUpperCase()}
                </span>
              </div>
              <div>
                <h3 className="text-2xl font-metamorphous font-bold text-white leading-none">
                  Sets of {playerDisplayName}
                </h3>
                <p className="text-sm text-gray-400 mt-1">
                  {requestedPlayerSets.length || 0} sets
                </p>
              </div>
            </div>

            <button
              onClick={() => setIsModalOpen(false)}
              className="text-gray-400 hover:text-white transition-colors text-2xl"
            >
              ✕
            </button>
          </div>

          {/* Content (llena el espacio disponible) */}
          <div className="flex-1 overflow-auto bg-slate-900/70 p-8">
            {requestedPlayerSets && requestedPlayerSets.length > 0 ? (
              <div className="overflow-x-auto py-4 px-2">
                {requestedPlayerSets.map((set, index) => (
                  <div
                    key={set?.set_play_id || index}
                    className="flex flex-col items-center p-7 w-full h-[300px]"
                    onClick={() => {
                      if (isInteractive) {
                        onSelectSet(set);
                        setIsModalOpen(false);
                      }
                    }}
                  >
                    {/* abanico de sets */}
                    <div className="flex-1 flex items-center justify-center w-full">
                      <div
                        className="relative flex justify-center items-end"
                        style={{ height: "120px" }}
                      >
                        {(set.card_game_images || []).map((image, index) => {
                          const rotation =
                            (index - (set.card_game_images.length - 1) / 2) * 5;
                          const translateY =
                            Math.abs(
                              index - (set.card_game_images.length - 1) / 2
                            ) * 4;
                          const left =
                            index * 50 -
                            ((set.card_game_images.length - 1) * 50) / 2;

                          return (
                            <div
                              key={
                                set.card_game_ids
                                  ? set.card_game_ids[index]
                                  : index
                              }
                              className="absolute transition-transform duration-300 hover:scale-110"
                              style={{
                                transform: `rotate(${rotation}deg) translateY(${translateY}px)`,
                                transformOrigin: "bottom center",
                                left: `${left}px`,
                              }}
                            >
                              <Card
                                image={image}
                                alt="SetCard"
                                size="w-30 h-42"
                              />
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-400 font-metamorphous">
                  This player doesn’t have sets
                </p>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="bg-slate-950/80 px-8 py-5 flex flex-col sm:flex-row-reverse items-center gap-3 border-t border-gray-800/80">
            <button
              onClick={() => setIsModalOpen(false)}
              className="inline-flex items-center justify-center rounded-xl px-8 py-3 text-sm font-metamorphous font-semibold shadow-[0_0_6px_#c2a22d] transition-all"
              style={{ background: "#c2a22d", color: "black" }}
              onMouseOver={(e) => {
                e.currentTarget.style.filter = "brightness(0.95)";
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.filter = "none";
              }}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
}
