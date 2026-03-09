import { createHttpService } from "../../../../services/HTTPServices";
import { emitSelectPlayer } from "../../../../websocket/emitters/CardEmitter";
import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { usePointYourSuspicionsStore } from "../../../../Store/PointYourSuspicionsStore";

export default async function playPointYourSuspicions(card, context) {
  if (!card) return {};
  const { id, name } = card;
  const { gameId, playerId, playersNumber } = context;
  const httpService = createHttpService();

  const { clearEventCardClicked } = useEventCardStore.getState();
  const {
    waitForAllPlayersSelected,
    setPlayerId,
    setExpectedPlayers,
    clearSelectedPlayers,
  } = usePointYourSuspicionsStore.getState();

  setPlayerId(playerId);
  setExpectedPlayers(playersNumber);

  // Emit point your suspicions - select player
  emitSelectPlayer(gameId, playerId, "Point Your Suspicions", name, "Event");

  // Wait to all players to vote
  const players = await waitForAllPlayersSelected(playersNumber);

  const targerPlayersIds = players.map((player) => player.target_player_id);

  await httpService.pointYourSuspicions(gameId, playerId, id, targerPlayersIds);

  clearSelectedPlayers();
  clearEventCardClicked();
}
