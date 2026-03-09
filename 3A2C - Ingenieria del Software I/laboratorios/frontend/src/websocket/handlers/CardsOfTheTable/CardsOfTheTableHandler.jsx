import toast from "react-hot-toast";

export function offTheTableHandler(payload, playerId, players) {
  const { player_id, target_player_id, card_name } = payload;

  const player = players.find((p) => p.id_jugador === player_id);
  const target = players.find((p) => p.id_jugador === target_player_id);

  const playerName = player?.nombre || "Unknown";
  const targetName = target?.nombre || "Unknown";

  if (target_player_id === playerId) {
    toast.remove();
    toast.error(
      `${playerName} played ${card_name} against you! You lose all your Not So Fast cards.`
    );
  } else {
    toast.remove();
    toast(
      `${playerName} played ${card_name} against ${targetName}. ${targetName} loses all their Not So Fast cards.`
    );
  }
}
