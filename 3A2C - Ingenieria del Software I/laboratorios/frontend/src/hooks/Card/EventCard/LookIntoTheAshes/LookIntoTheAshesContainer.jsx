import { createHttpService } from "../../../../services/HTTPServices";
import { emitSelectCard } from "../../../../websocket/emitters/CardEmitter";
import { intoTheAshesStore } from "../../../../Store/IntoTheAshesStore";
import { useEventCardStore } from "../../../../Store/useEventCardStore";

export default async function playLookIntoTheAshes(card, context) {
  if (!card) return {};
  const { id, name } = card;
  const { gameId, playerId } = context;
  const httpService = createHttpService();

  const { clearEventCardClicked } = useEventCardStore.getState();
  const { setOpenModal, waitForSelectedCardToDraw } =
    intoTheAshesStore.getState();

  setOpenModal(true);

  const selectedCardToDraw = await waitForSelectedCardToDraw();

  await httpService.lookIntoTheAshes(gameId, playerId, id, selectedCardToDraw);

  clearEventCardClicked();
}
