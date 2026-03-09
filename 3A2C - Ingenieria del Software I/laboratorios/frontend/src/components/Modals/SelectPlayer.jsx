import { useState } from "react";
import { useEventCardStore } from "../../Store/useEventCardStore";
import { usePointYourSuspicionsStore } from "../../Store/PointYourSuspicionsStore";
import { resolveSelectPlayer } from "../../websocket/emitters/CardEmitter";
import toast from "react-hot-toast";

export default function SelectPlayerModal({
  players,
  playerId,
  effect,
  onConfirm,
}) {
  const [selectedId, setSelectedId] = useState(null);
  const selectedPlayer = players.find((p) => p.id_jugador === selectedId);

  // Evend Card Logic
  const { setTargetPlayer, setSelectPlayer, selectPlayer } =
    useEventCardStore();
  const {
    selectPlayerSuspicions,
    setSelectPlayerSuspicions,
    selectPlayerInfo,
    setSelectPlayerInfo,
  } = usePointYourSuspicionsStore();

  const handleSelect = () => {
    if (!selectedPlayer) return;

    if (selectPlayer) {
      // Update global store
      setTargetPlayer({
        id: selectedPlayer.id_jugador,
        name: selectedPlayer.nombre,
      });
      setSelectPlayer(false);

      // Point your suspicions compatibility
    } else if (selectPlayerSuspicions) {
      // select player
      resolveSelectPlayer(
        selectPlayerInfo.game_id,
        playerId,
        selectedPlayer.id_jugador,
        selectedPlayer.nombre,
        selectPlayerInfo.player_id
      );
      toast.success(`You voted for ${selectedPlayer.nombre}`);
      setSelectPlayerSuspicions(false);
      setSelectPlayerInfo(null);
    }

    // Compatibility with selectPlayer for Set
    onConfirm?.({
      id: selectedPlayer.id_jugador,
      name: selectedPlayer.nombre,
    });
  };

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/70">
      <div className="bg-slate-900 p-6 rounded-xl shadow-xl w-[400px] border border-yellow-500">
        <h2 className="text-2xl font-metamorphous text-white mb-4 text-center">
          Choose a player
        </h2>

        <ul className="space-y-3 mb-6">
          {players.map((p) => {
            const canSelect =
              (effect === "Reveal by Target" && p.id_jugador !== playerId) ||
              (effect === "Reveal by Actor" && p.id_jugador !== playerId) ||
              effect === "Hide" ||
              (effect === "Steal" && p.id_jugador !== playerId) ||
              (effect === "Ariadne Oliver" && p.id_jugador !== playerId) || // Change this, Ariadne hanlde all existings Sets
              (effect === "EventCard" && p.id_jugador !== playerId) ||
              effect === "OneMore" ||
              (effect === "Point Your Suspicions" && p.id_jugador !== playerId);
            return (
              <li key={p.id_jugador}>
                <button
                  onClick={() => canSelect && setSelectedId(p.id_jugador)}
                  className={`w-full px-4 py-2 rounded-md transition-all font-metamorphous
                  ${
                    selectedId === p.id_jugador
                      ? "bg-yellow-500 text-black font-bold"
                      : "bg-[#0b3b6f] text-white hover:bg-[#c2a22d] hover:text-black"
                  }`}
                >
                  {p.nombre}
                </button>
              </li>
            );
          })}
        </ul>

        <div className="flex justify-center">
          <button
            onClick={handleSelect}
            disabled={!selectedPlayer}
            className={`px-6 py-2 rounded-md font-metamorphous transition-all shadow-[0_0_6px_#c2a22d]
              ${
                selectedPlayer
                  ? "bg-yellow-500 text-black hover:brightness-95"
                  : "bg-gray-700 text-gray-400 cursor-not-allowed"
              }`}
          >
            Select
          </button>
        </div>
      </div>
    </div>
  );
}
