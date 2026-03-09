import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { delayMurderEscapesStore } from "../../../../Store/DelayMurderEscapesStore";
import { createHttpService } from "../../../../services/HTTPServices";
import { emitSelectCard } from "../../../../websocket/emitters/CardEmitter";

export default async function playDelayMurderEscaped(card, context) {
  const { id, name } = card;
  const { gameId, playerId } = context;

  const httpService = createHttpService();
  const { clearEventCardClicked } = useEventCardStore.getState();
  const { setOpenDiscardModal, waitForDiscardCardSelection } =
    delayMurderEscapesStore.getState();

  // Open discard pile modal
  setOpenDiscardModal(true);

  const cards = await waitForDiscardCardSelection();

  // Endpoint call
  await httpService.murdererEscapes(gameId, playerId, cards, id);

  clearEventCardClicked();
}
