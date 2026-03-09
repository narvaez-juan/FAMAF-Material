import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { useAnotherVictimStore } from "../../../../Store/AnotherVictimStore";
import { createHttpService } from "../../../../services/HTTPServices";

export default async function playAnotherVictim(card, context) {
  const { id, name } = card;
  const { gameId, playerId } = context;
  const httpService = createHttpService();

  const { clearEventCardClicked } = useEventCardStore.getState();
  const {
    setselectPlayerToStealSet,
    waitForTargetPlayerToStealSet,
    waitForTargetSetToStealId,
    setNewStolenSet,
  } = useAnotherVictimStore.getState();

  setselectPlayerToStealSet(true);

  // Wait until player is selected
  const player = await waitForTargetPlayerToStealSet();

  console.log("Another Victim selected player:", player);

  const stolenSet = await waitForTargetSetToStealId();

  console.log("Another Victim selected set id:", stolenSet);

  // Endpoint call - this only get the new stolen set - playerHand container will play it
  const newStolenSet = await httpService.anotherVictim(
    gameId,
    playerId,
    stolenSet,
    id
  );

  // this will set the new stolen set in the store for the PlayerHand container to pick it up
  setNewStolenSet(newStolenSet);

  clearEventCardClicked();
}
