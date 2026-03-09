import { useEventCardStore } from "../../../Store/useEventCardStore";
import toast from "react-hot-toast";

export function delayMurderEscapedHandler(payload, playerId, players) {
  const { player_id, card_name } = payload;

  const player = players.find((p) => p.id_jugador === player_id);

  const playerName = player?.nombre || "Unknown";

  if (player_id !== playerId) {
    toast.remove();
    toast(
      `${playerName} played ${card_name}. Five cards from the discard pile were moved to the draw pile!`,
      {
        icon: "🐌",
      }
    );
  } else {
    toast.remove();
    toast.success(
      `You played ${card_name}. Five cards were moved from the discard pile to the draw pile!`
    );
  }
}
