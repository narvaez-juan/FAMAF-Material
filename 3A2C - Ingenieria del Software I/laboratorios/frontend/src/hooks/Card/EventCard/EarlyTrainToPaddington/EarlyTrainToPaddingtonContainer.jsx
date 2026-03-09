import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { createHttpService } from "../../../../services/HTTPServices";
import { emitSelectCard } from "../../../../websocket/emitters/CardEmitter";

export default async function useEarlyTrainToPaddington(card, context) {
  if (!card) return {};
  const { id, name } = card;
  const { gameId, playerId } = context;
  const httpService = createHttpService();

  const { clearEventCardClicked } = useEventCardStore.getState();

  // Emit card played event
  const cardType = "Event";
  const cardName = "Early Train to Paddington";
  emitSelectCard(gameId, playerId, cardName, name, null, cardType);

  // Call backend endpoint
  await httpService.earlyTrainToPaddington(gameId, playerId, id);

  clearEventCardClicked();
}
