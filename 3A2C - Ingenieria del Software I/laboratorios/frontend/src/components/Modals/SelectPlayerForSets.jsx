import React, { useState } from "react";

export default function SelectPlayerToStealSetModal({
  players = [],
  playerId,
  onConfirm,
  onCancel,
}) {
  const [selectedId, setSelectedId] = useState(null);

  const playersToStealFrom = players.filter(
    (p) => String(p.id_jugador) !== String(playerId)
  );

  const selectedPlayer = playersToStealFrom.find(
    (p) => p.id_jugador === selectedId
  );

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/70">
      <div className="bg-slate-900 p-6 rounded-xl shadow-xl w-[400px] border border-yellow-500">
        <h2 className="text-2xl font-metamorphous text-white mb-4 text-center">
          Select a player to steal
        </h2>

        <ul className="space-y-3 mb-6 max-h-64 overflow-y-auto">
          {playersToStealFrom.length === 0 ? (
            <li>
              <div className="w-full px-4 py-2 rounded-md bg-[#0b3b6f] text-white text-center">
                There are no other players to steal from.
              </div>
            </li>
          ) : (
            playersToStealFrom.map((p) => {
              const isSelected = selectedId === p.id_jugador;
              return (
                <li key={p.id_jugador}>
                  <button
                    onClick={() => setSelectedId(p.id_jugador)}
                    className={`w-full px-4 py-2 rounded-md transition-all font-metamorphous
                      ${
                        isSelected
                          ? "bg-yellow-500 text-black font-bold"
                          : "bg-[#0b3b6f] text-white hover:bg-[#c2a22d] hover:text-black"
                      } flex items-center justify-between`}
                    aria-pressed={isSelected}
                  >
                    <span>{p.nombre || `Player ${p.id_jugador}`}</span>
                    <span className="text-xs">
                      {isSelected ? (
                        <span className="px-2 py-0.5 rounded bg-black/10 text-black font-semibold">
                          Selected
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded text-yellow-200">
                          Choose
                        </span>
                      )}
                    </span>
                  </button>
                </li>
              );
            })
          )}
        </ul>

        <div className="flex justify-center gap-4">
          <button
            onClick={() => onCancel && onCancel()}
            className="px-6 py-2 rounded-md font-metamorphous transition-all bg-gray-700 text-gray-200 hover:bg-gray-600"
          >
            Cancel
          </button>

          <button
            onClick={() => selectedPlayer && onConfirm(selectedPlayer)}
            disabled={!selectedPlayer}
            className={`px-6 py-2 rounded-md font-metamorphous transition-all shadow-[0_0_6px_#c2a22d]
              ${
                selectedPlayer
                  ? "bg-yellow-500 text-black hover:brightness-95"
                  : "bg-gray-700 text-gray-400 cursor-not-allowed"
              }`}
          >
            Confirm Steal
          </button>
        </div>
      </div>
    </div>
  );
}
