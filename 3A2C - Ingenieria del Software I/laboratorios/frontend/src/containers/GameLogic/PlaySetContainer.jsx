import { useState, useEffect, useRef, useCallback } from "react";
import { createHttpService } from "../../services/HTTPServices";
import getSocket from "../../services/WSServices";

export default function useSets(gameId, playerId) {
  const [httpService] = useState(() => createHttpService());
  const [allSets, setAllSets] = useState([]);
  const [requestedPlayerSets, setRequestedPlayerSets] = useState([]);
  const [selectRequest, setSelectRequest] = useState(null);
  const [ownerSecretRequest, setOwnerSecretRequest] = useState(null);
  const [targetSecretRequest, setTargetSecretRequest] = useState(null);
  const [isLoadingSets, setIsLoadingSets] = useState(false);
  const [error, setError] = useState(null);

  const socketRef = useRef(null);
  const pendingPlayerIdRef = useRef(null);
  const emitPlayerSetsHandlerRef = useRef(null);

  useEffect(() => {
    let connectHandler = null;

    const initSocket = async () => {
      try {
        if (!localStorage.getItem("RoomID") && gameId) {
          localStorage.setItem("RoomID", gameId);
        }

        const sock = await getSocket();
        socketRef.current = sock;

        const requestAllSets = () => {
          if (!gameId) return;
          sock.emit("get_all_sets", { game_id: gameId });
        };

        connectHandler = () => {
          requestAllSets();
        };

        // Update all sets played (global broadcast)
        sock.on("player_sets_updated", (payload) => {
          setAllSets(payload.players_sets);
        });

        // Owner chooses secret (to reveal or hide)
        sock.on("owner_chooses_secret", (payload) => {
          if (payload.owner_id === playerId) {
            setOwnerSecretRequest(payload);
          }
        });

        // Target chooses secret (to reveal)
        sock.on("target_chooses_secret", (payload) => {
          if (payload.target_id === playerId) {
            setTargetSecretRequest(payload);
          }
        });

        // Request specific sets from a single player
        const handleEmitPlayerSets = (payload) => {
          const payloadPlayerId = payload?.player_id ?? payload?.playerId;
          const normalizedPayloadId =
            payloadPlayerId != null ? Number(payloadPlayerId) : null;
          const normalizedPendingId =
            pendingPlayerIdRef.current != null
              ? Number(pendingPlayerIdRef.current)
              : null;

          if (
            normalizedPendingId != null &&
            normalizedPayloadId != null &&
            normalizedPayloadId !== normalizedPendingId
          ) {
            return;
          }

          setRequestedPlayerSets(payload.sets);
          setIsLoadingSets(false);
          if (
            normalizedPendingId != null &&
            normalizedPayloadId === normalizedPendingId
          ) {
            pendingPlayerIdRef.current = null;
          }
        };

        emitPlayerSetsHandlerRef.current = handleEmitPlayerSets;
        sock.on("emit_player_sets", handleEmitPlayerSets);

        if (sock.connected) {
          requestAllSets();
        } else {
          sock.on("connect", connectHandler);
        }
      } catch (err) {
        console.error("Error al conectar socket:", err);
        setError("WebSocket connection failed");
      }
    };

    if (gameId && playerId) {
      initSocket();
    }

    return () => {
      const sock = socketRef.current;
      if (sock) {
        sock.off("player_sets_updated");
        const handler = emitPlayerSetsHandlerRef.current;
        if (handler) {
          sock.off("emit_player_sets", handler);
          emitPlayerSetsHandlerRef.current = null;
        }
        if (connectHandler) sock.off("connect", connectHandler);
      }
    };
  }, [gameId, playerId]);

  const fetchPlayerSets = useCallback(
    async (targetPlayerId) => {
      try {
        if (!gameId) return;

        if (!socketRef.current) {
          const sock = await getSocket();
          socketRef.current = sock;
        }

        setIsLoadingSets(true);
        pendingPlayerIdRef.current = targetPlayerId;
        socketRef.current.emit("get_player_sets", {
          game_id: gameId,
          player_id: targetPlayerId,
        });
      } catch (err) {
        console.error("fetchPlayerSets failed:", err);
        setIsLoadingSets(false);
      }
    },
    [gameId]
  );

  const playSet = async (selectedCards) => {
    try {
      setIsLoadingSets(true);
      const response = await httpService.setPlay(
        gameId,
        playerId,
        selectedCards
      );
      return response;
    } catch (err) {
      console.error("Error al jugar set:", err);
      setError("No se pudo jugar el set");
      throw err;
    } finally {
      setIsLoadingSets(false);
    }
  };

  return {
    allSets,
    requestedPlayerSets,
    selectRequest,
    fetchPlayerSets,
    playSet,
    isLoadingSets,
    error,
  };
}
