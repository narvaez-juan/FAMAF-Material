import toast from "react-hot-toast";

export function earlyTrainHandler(payload, playerId, players) {
  const { player_id, card_name } = payload;

  const player = players.find((p) => p.id_jugador === player_id);
  const playerName = player?.nombre || "Unknown";

  toast.remove();

  if (player_id === playerId) {
    toast.success(
      `You played ${card_name}. Six cards were discarded from the deck!`
    );
  } else {
    toast(
      `${playerName} played ${card_name}. Six cards were discarded from the deck!`,
      { icon: "🚂" }
    );
  }
}
