import toast from "react-hot-toast";
import { emitSecrets } from "../../../../services/WSServices";
import { useEventCardStore } from "../../../../Store/useEventCardStore";

export function handleDeviousCard(payload, playerId) {
  // Only show toast if the card is for the current player
  if (payload.player_id !== playerId) {
    return;
  }

  if (payload.source_card === "Social Faux Pas") {
    handleSocialFauxPas(payload, playerId);
  }
}

export function handleSocialFauxPas(payload, playerId) {
  const { setVotedToReveal, setVotedPlayerId, setSecrets } =
    useEventCardStore.getState();

  const toastId = `social-faux-pas-${playerId}`;

  toast.dismiss(toastId);

  setTimeout(() => {
    toast(
      "You received the 'Social Faux Pas' card! You must reveal a secret of your choice.",
      {
        icon: "❗",
        id: toastId,
      }
    );
  }, 0);

  // clear secrets
  setSecrets(null);

  // Get secrets - this will set "secrets"
  emitSecrets(payload.game_id, playerId);

  // Set player Id to see his secrets
  setVotedPlayerId(playerId);

  // Open modal to select secret
  setVotedToReveal(true);
}
