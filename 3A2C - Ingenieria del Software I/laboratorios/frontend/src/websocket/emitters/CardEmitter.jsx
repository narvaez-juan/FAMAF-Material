import { emit } from "../../services/WSServices.js";

export function emitSelectCard(
  gameId,
  playerId,
  cardName,
  cardImage,
  direction,
  cardType
) {
  const payload = {
    event: "card_played_event",
    game_id: gameId,
    player_id: playerId,
    card_name: cardName,
    card_image: cardImage,
    card_type: cardType,
    direction: direction,
  };
  emit("select_card", payload);
}

export function resolveSelectCard(
  gameId,
  playerId,
  cardId,
  cardImage,
  requesterId
) {
  emit("resolve_select_card", {
    game_id: gameId,
    player_id: playerId,
    card_id: cardId,
    card_image: cardImage,
    requester_id: requesterId,
  });
}

export function emitSelectPlayer(
  gameId,
  playerId,
  cardName,
  cardImage,
  cardType
) {
  const payload = {
    event: "card_played_event",
    game_id: gameId,
    player_id: playerId,
    card_name: cardName,
    card_image: cardImage,
    card_type: cardType,
  };
  emit("select_player", payload);
}

export function resolveSelectPlayer(
  gameId,
  playerId,
  targetPlayerId,
  targetName,
  requesterId
) {
  const payload = {
    game_id: gameId,
    player_id: playerId,
    target_player_id: targetPlayerId,
    target_name: targetName,
    requester_id: requesterId,
  };

  emit("resolve_select_player", payload);
}
