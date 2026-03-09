import { useState } from "react";
import { createHttpService } from "../../services/HTTPServices";

export default function useDrawCard() {
  const [httpService] = useState(() => createHttpService());

  const drawCard = async (
    game_id,
    player_id,
    selectedDraftCards,
    selectedDrawCardsNumber
  ) => {
    return await httpService.drawCard(
      game_id,
      player_id,
      selectedDraftCards,
      selectedDrawCardsNumber
    );
  };

  return drawCard;
}
