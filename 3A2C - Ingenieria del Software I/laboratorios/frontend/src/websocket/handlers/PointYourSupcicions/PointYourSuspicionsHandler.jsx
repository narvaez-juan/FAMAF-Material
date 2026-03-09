import { usePointYourSuspicionsStore } from "../../../Store/PointYourSuspicionsStore";
import { useEventCardStore } from "../../../Store/useEventCardStore";
import toast from "react-hot-toast";
import { emitSecrets } from "../../../services/WSServices";

export function handleSelectPlayerPayload(payload) {
  if (payload.card_name !== "Point Your Suspicions") return;
  const { setSelectPlayerSuspicions, setSelectPlayerInfo } =
    usePointYourSuspicionsStore.getState();
  setSelectPlayerInfo(payload);
  setSelectPlayerSuspicions(true);
}

export function handleSelectPlayerResolve(payload, playerId) {
  if (payload && payload.requester_id === playerId) {
    const { setSelectedPlayers } = usePointYourSuspicionsStore.getState();
    setSelectedPlayers(payload);
  }
}

export function handleSecretsPayload(payload) {
  const { setSecrets } = useEventCardStore.getState();
  setSecrets(payload.player_id, payload);
}

export function PointYourSuspicionsHandler(payload, playerId, players) {
  if (!payload) return;

  const { setVotedToReveal, setVotedPlayerId } = useEventCardStore.getState();

  const { player_id, target_player_id, card_name } = payload;

  const actingPlayer = players.find((p) => p.id_jugador === player_id);
  const actingPlayerName = actingPlayer?.nombre || "Unknown";

  const targetPlayer = players.find((p) => p.id_jugador === target_player_id);
  const targetPlayerName = targetPlayer?.nombre || "Unknown";

  toast.remove();

  if (target_player_id === playerId) {
    // El jugador actual fue el seleccionado
    toast.error(
      `${actingPlayerName} played ${card_name}! You have been selected to reveal a secret!`,
      { icon: "❗" }
    );

    emitSecrets(payload.game_id, target_player_id);
    setVotedToReveal(true);
    setVotedPlayerId(target_player_id);
  } else if (player_id === playerId) {
    // El jugador actual fue quien jugó la carta
    toast.success(
      `You played ${card_name}! The group voted and ${targetPlayerName} has been selected to reveal a secret.`
    );
  } else {
    // Observador
    toast(
      `${actingPlayerName} played ${card_name}! The group voted and ${targetPlayerName} has been selected to reveal a secret.`,
      { icon: "🕵️" }
    );
  }
}
