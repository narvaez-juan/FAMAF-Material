import { useState, useCallback } from "react";

export default function useAriadneFlow({
  gameId,
  playerId,
  fetchPlayerSets,
  httpService,
}) {
  const [ariadneContext, setAriadneContext] = useState(null);

  // Called when the player chooses a target for Ariadne
  const handleAriadne = useCallback(
    (player, ariadneCardId) => {
      if (!player) return;

      console.log("useAriadneFlow.handleAriadne called", {
        player,
        ariadneCardId,
      });

      const cardId =
        ariadneCardId || (ariadneContext && ariadneContext.ariadneCardId);

      setAriadneContext({
        ariadneCardId: cardId,
        jugador: {
          id_jugador: player.id || player.id_jugador || player.player_id,
          nombre: player.name || player.nombre,
        },
      });
    },
    [fetchPlayerSets, ariadneContext]
  );

  // Called when the user selects a set from the target player's sets
  const handlePlayAriadne = useCallback(
    async (set) => {
      if (!set) throw new Error("No set provided to playAriadne");
      if (!httpService)
        throw new Error("httpService is required to play Ariadne");

      const payload = {
        AriadneCardId: ariadneContext?.ariadneCardId,
        targetSetId: set.set_play_id,
        playerId,
      };

      const res = await httpService.playAriadne(gameId, payload);

      // clear local context after playing
      setAriadneContext(null);

      return res;
    },
    [httpService, gameId, playerId, ariadneContext]
  );

  return {
    ariadneContext,
    handleAriadne,
    handlePlayAriadne,
    setAriadneContext,
  };
}
