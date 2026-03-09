import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { createHttpService } from "../../../../services/HTTPServices";

export default async function useCardsOnTheTable(card, context) {
  const { id, name } = card;
  const { gameId, playerId } = context;
  const httpService = createHttpService();

  const {
    setSelectPlayer,
    waitForTargetPlayer,
    eventCardClicked,
    clearEventCardClicked,
  } = useEventCardStore.getState();

  // Request choose a player
  setSelectPlayer(true);

  // Wait until player is selected
  const player = await waitForTargetPlayer();

  // Endpoint call
  await httpService.cardsOfTheTable(
    gameId,
    playerId,
    eventCardClicked.id,
    player.id
  );

  clearEventCardClicked();
}
