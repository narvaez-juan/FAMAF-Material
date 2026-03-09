import { useDeadCardFollyStore } from "../../../Store/DeadCardFollyStore";
import { useEventCardStore } from "../../../Store/useEventCardStore";
import toast from "react-hot-toast";

export function handleSelectCardPayload(payload) {
  if (payload.card_name !== "Dead Card Folly") return;
  const { setSelectCardInfo, setSelectCard } = useDeadCardFollyStore.getState();
  setSelectCardInfo(payload);
  setSelectCard(true);
}

export function handleSelectCardResolve(payload) {
  if (payload) {
    const { setSelectedCardsByPlayers } = useDeadCardFollyStore.getState();
    setSelectedCardsByPlayers(payload);
  }
}

export function deadCardFollyHandler(payload, playerId, players) {
  const { player_id, card_name } = payload;

  const player = players.find((p) => p.id_jugador === player_id);

  const playerName = player?.nombre || "Unknown";

  const toastId = `dead-card-folly-${player_id}`;

  if (player_id !== playerId) {
    //toast.remove();
    toast(`${playerName} played ${card_name}! All players passed one card.`, {
      icon: "🧙‍♂️",
      id: toastId,
    });
  } else {
    //toast.remove();
    toast.success(
      `you played ${card_name} successfully!. All players passed one card.`,
      { id: toastId }
    );
  }
}
