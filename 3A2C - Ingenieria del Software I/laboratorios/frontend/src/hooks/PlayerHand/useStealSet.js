import { useCallback, useEffect, useState } from "react";
import { useAnotherVictimStore } from "../../Store/AnotherVictimStore";
import toast from "react-hot-toast";

export default function useStealSet({
  gameId,
  playerId,
  fetchPlayerSets,
  requestedPlayerSets,
  isLoadingSets,
  httpService,
  isMyTurn,
  setTurnAction,
}) {
  const [isSelectStealTargetOpen, setIsSelectStealTargetOpen] = useState(false);
  const [isSelectSetToStealOpen, setIsSelectSetToStealOpen] = useState(false);
  const [stealTargetPlayer, setStealTargetPlayer] = useState(null);
  const [targetPlayerSets, setTargetPlayerSets] = useState([]);
  const [loadingTargetSets, setLoadingTargetSets] = useState(false);

  // Store
  const {
    setselectPlayerToStealSet,
    setTargetPlayerToStealSet,
    setSelectSetToStealOpen,
    setTargetSetToStealId,
  } = useAnotherVictimStore.getState();

  const targetPlayerToStealSet = useAnotherVictimStore(
    (state) => state.targetPlayerToStealSet
  );

  // ACA SELECCIONAMOS AL JUGADOR PARA ROBARLE EL SET
  const handleSelectStealTarget = useCallback(
    (targetPlayer) => {
      const targetPlayerId =
        targetPlayer?.id || targetPlayer?.id_jugador || targetPlayer?.player_id;
      if (!targetPlayerId) {
        console.error(
          "[useStealSet] could not resolve target player id from:",
          targetPlayer
        );
        alert("Cannot determine target player id");
        return;
      }

      setTargetPlayerToStealSet(targetPlayer);
      setselectPlayerToStealSet(false);
      setLoadingTargetSets(true);

      console.log("[useStealSet] selected target player:", targetPlayer);

      try {
        fetchPlayerSets(targetPlayerId);
      } catch (err) {
        console.error("[useStealSet] fetchPlayerSets error:", err);
        alert("Error al obtener los sets del jugador");
        setTargetPlayerToStealSet(null);
        setLoadingTargetSets(false);
      }
    },
    [fetchPlayerSets]
  );

  // react to fetch results coming from `requestedPlayerSets` + `isLoadingSets`

  // ACA SE ABRE EL MODAL PARA ROBAR EL SET
  useEffect(() => {
    if (!targetPlayerToStealSet) return;

    if (!isLoadingSets && targetPlayerToStealSet) {
      if (requestedPlayerSets && requestedPlayerSets.length > 0) {
        setTargetPlayerSets(requestedPlayerSets);
        setSelectSetToStealOpen(true);
        setLoadingTargetSets(false);
      } else if (requestedPlayerSets && requestedPlayerSets.length === 0) {
        // toast
        toast.error(
          `${
            targetPlayerToStealSet.nombre || "The player"
          } has no sets to steal.`
        );
        setTargetPlayerToStealSet(null);
        setLoadingTargetSets(false);
        setSelectSetToStealOpen(false);
      }
    }
  }, [isLoadingSets, requestedPlayerSets, targetPlayerToStealSet]);

  // ACA SELECCIONAMOS EL SET A ROBAR
  const handleSelectSetToSteal = useCallback(
    async (setId) => {
      try {
        if (typeof setTurnAction === "function") setTurnAction("stealing");
        await httpService.stealSet(gameId, playerId, setId);
        setSelectSetToStealOpen(false); // cambiado a store
        setTargetPlayerToStealSet(null);
        setTargetPlayerSets([]);
        setTargetSetToStealId(setId);
        setLoadingTargetSets(false);
        if (typeof setTurnAction === "function") setTurnAction("idle");
      } catch (error) {
        console.error("[useStealSet] Error robando set:", error);
        alert("Error al robar el set");
        if (typeof setTurnAction === "function") setTurnAction("idle");
      }
    },
    [httpService, gameId, playerId, setTurnAction]
  );

  return {
    isSelectStealTargetOpen,
    setIsSelectStealTargetOpen,
    isSelectSetToStealOpen,
    setIsSelectSetToStealOpen,
    stealTargetPlayer,
    targetPlayerSets,
    loadingTargetSets,
    handleSelectStealTarget,
    handleSelectSetToSteal,
  };
}
