import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { createHttpService } from "../../../../services/HTTPServices";
import { emitSelectCard } from "../../../../websocket/emitters/CardEmitter";
import { useDeadCardFollyStore } from "../../../../Store/DeadCardFollyStore";

export default async function useDeadCardFolly(card, context) {
  if (!card) return {};
  const { id, name } = card;
  const { gameId, playerId, playersNumber } = context;
  const httpService = createHttpService();

  const { clearEventCardClicked } = useEventCardStore.getState();

  const { setExpectedPlayers, waitForAllCardsSelected, waitForDirection } =
    useDeadCardFollyStore.getState();

  useDeadCardFollyStore.setState({ selectedCardsByPlayers: [] });
  setExpectedPlayers(playersNumber);

  // Select direction
  const direction = await waitForDirection();

  // Emit dead card folly -  select cards
  const cardType = "Event";
  const cardName = "Dead Card Folly";
  emitSelectCard(gameId, playerId, cardName, name, direction, cardType);

  // All cards are ready
  const allSelectedCards = await waitForAllCardsSelected(playersNumber);

  // Endpoint call
  const cardsToPass = allSelectedCards.map((c) => [c.player_id, c.card_id]);
  await httpService.deadCardFolly(gameId, direction, cardsToPass, id);

  clearEventCardClicked();
}
