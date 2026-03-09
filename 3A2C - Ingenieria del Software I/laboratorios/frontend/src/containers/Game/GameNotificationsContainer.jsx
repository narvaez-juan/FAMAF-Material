import { useEffect, useState, useRef, useCallback } from "react";
import getSocket from "../../services/WSServices";

export default function useGameNotification(gameId) {
  const [gameNotification, setGameNotification] = useState();
  const [secretNotification, setSecretNotification] = useState();
  const [selectSecretRequest, setSelectSecretRequest] = useState();
  const [ariadneNotification, setAriadneNotification] = useState();

  const handleHandPayload = (payload) => {
    if (
      payload &&
      (payload.type === "game_finished" || payload.winner !== undefined)
    ) {
      setGameNotification(payload);
    } else if (
      payload &&
      (payload.type === "secret_selection_modal" ||
        payload.type === "secret_reveal_modal")
    ) {
      setSecretNotification(payload);
    }
  };

  const handleSelectSecret = (payload) => {
    if (payload) {
      setSelectSecretRequest(payload);
    }
  };

  const handleAriadnePayload = (payload) => {
    if (payload) {
      setAriadneNotification(payload);
    }
  };

  const handleMurdererRevealed = (payload) => {
    if (payload) {
      setGameNotification({
        type: "game_finished",
        payload: {
          reason: "The murderer has been revealed",
          actor_id: payload.actor_id,
          target_id: payload.target_id,
          secret_id: payload.secret_id,
          secret_name: payload.secret_name,
        },
      });
    }
  }

  const socketRef = useRef(null);

  useEffect(() => {
    const connect = async () => {
      try {
        const sock = await getSocket();
        socketRef.current = sock;

        // ya estoy conectado
        sock.on("notify_winner", handleHandPayload);
        sock.on("selecting_secret", handleHandPayload);
        sock.on("secret_resolved", handleHandPayload);
        sock.on("murderer_revealed", handleMurdererRevealed);
        sock.on("select_secret_request", handleSelectSecret);
        sock.on("choose_target_for_ariadne", handleAriadnePayload);

        // reconexion
        if (sock.connected) {
          sock.on("notify_winner", handleHandPayload);
          sock.on("selecting_secret", handleHandPayload);
          sock.on("secret_resolved", handleHandPayload);
          sock.on("murderer_revealed", handleMurdererRevealed);
          sock.on("select_secret_request", handleSelectSecret);
          sock.on("choose_target_for_ariadne", handleAriadnePayload);
        } else {
          // conexion nueva
          sock.on("connect", () => {
            sock.on("notify_winner", handleHandPayload);
            sock.on("selecting_secret", handleHandPayload);
            sock.on("secret_resolved", handleHandPayload);
            sock.on("murderer_revealed", handleMurdererRevealed);
            sock.on("select_secret_request", handleSelectSecret);
            sock.on("choose_target_for_ariadne", handleAriadnePayload);
          });
        }
      } catch (err) {
        console.error(
          "Socket connection in GameNotificationContainer failed:",
          err
        );
      }
    };

    connect();

    return () => {
      const sock = socketRef.current;
    };
  }, [gameId]);

  const emitWaitingModals = useCallback(
    (playerId, targetPlayerId, secretEffect) => {
      if (!socketRef.current || !gameId) return;
      socketRef.current.emit("get_waiting_modal", {
        game_id: gameId,
        target_player_id: targetPlayerId,
        player_id: playerId,
        secret_effect: secretEffect,
      });
    },
    [gameId]
  );

  const emitSecretResolved = useCallback(
    (playerId, targetPlayerId) => {
      if (!socketRef.current || !gameId) return;
      socketRef.current.emit("resolve_secret_modal", {
        game_id: gameId,
        player_id: playerId,
        target_player_id: targetPlayerId,
      });
    },
    [gameId]
  );

  return {
    gameNotification,
    emitWaitingModals,
    emitSecretResolved,
    secretNotification,
    selectSecretRequest,
    ariadneNotification,
  };
}
