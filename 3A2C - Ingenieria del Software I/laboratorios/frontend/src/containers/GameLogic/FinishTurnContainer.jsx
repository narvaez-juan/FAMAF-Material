import { useState } from "react";
import { createHttpService } from "../../services/HTTPServices";

export default function useFinishTurn() {
  const [httpService] = useState(() => createHttpService());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const finish = async (
    gameId,
    playerId,
    playerHasDiscarded,
    playerHasPlayedEvent,
    playerHand,
    cardsToDrawFromDeck
  ) => {
    setError(null);
    setLoading(true);
    try {
      if (!playerHasDiscarded && !playerHasPlayedEvent) {
        const cardToDiscardId =
          (playerHand && playerHand[1] && playerHand[1].gameCardId) ||
          (playerHand && playerHand[0] && playerHand[0].gameCardId);

        if (cardToDiscardId) {
          await httpService.discardCard(gameId, playerId, [cardToDiscardId]);
        }

        await httpService.drawCard(gameId, playerId, [], 1);
      }
      const response = await httpService.finishTurn(gameId, playerId);
      if (cardsToDrawFromDeck > 0) {
        const response1 = await httpService.drawCard(
          gameId,
          playerId,
          [],
          cardsToDrawFromDeck
        );
      }
    } catch (err) {
      if (err && err.status == 404) {
        console.log("Game not found");
      } else if (err && err.status == 400) {
        console.log("The game has not started yet");
      } else if (err && err.status == 403) {
        console.log("It is not your turn");
      }
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { finish, loading, error };
}
