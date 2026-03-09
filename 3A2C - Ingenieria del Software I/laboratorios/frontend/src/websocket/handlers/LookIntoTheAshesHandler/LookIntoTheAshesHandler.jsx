import toast from "react-hot-toast";

export function lookIntoTheAshesHandler(payload, playerId, players) {
  if (!payload) return;

  const { player_id, card_name } = payload;
  const player = players.find((p) => p.id_jugador === player_id);
  const playerName = player?.nombre || "Unknown";

  toast.remove();

  if (player_id !== playerId) {
    toast(
      `${playerName} played ${card_name} and took one card from the discard pile!`,
      {
        icon: "🦝",
      }
    );
  } else {
    toast.success(
      `You played ${card_name}! You took one card from the discard pile.`
    );
  }
}
