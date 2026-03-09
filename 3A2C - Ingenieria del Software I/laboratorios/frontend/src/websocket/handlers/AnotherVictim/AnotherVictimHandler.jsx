import toast from "react-hot-toast";

export function anotherVictimHandler(payload, playerId, players) {
  const { player_id, card_name } = payload;

  const player = players.find((p) => p.id_jugador === player_id);
  const playerName = player?.nombre || "Unknown";

  toast.remove();

  if (player_id !== playerId) {
    toast.error(
      `${playerName} played ${card_name} and stole a set! They are now playing it.`,
      {
        icon: "🦝",
      }
    );
  } else {
    toast.success(
      `You played ${card_name} and stole a set! Now you’re playing it.`
    );
  }
}
