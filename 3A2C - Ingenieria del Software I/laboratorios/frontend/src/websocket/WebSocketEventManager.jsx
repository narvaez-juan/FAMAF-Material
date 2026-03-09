import { useEffect, useState, useRef, useCallback } from "react";
import getSocket from "../services/WSServices";
import {
  handleSelectCardPayload,
  handleSelectCardResolve,
} from "./handlers/DeadCardFolly/DeadCardFollyHandler";
import {
  handleSelectPlayerPayload,
  handleSelectPlayerResolve,
  handleSecretsPayload,
} from "./handlers/PointYourSupcicions/PointYourSuspicionsHandler";
import { handleDeviousCard } from "./handlers/DeviousCard/SocialFauxPas/SocialFauxPasContainer";

export default function initWebSocketEventManager(gameId, playerId) {
  const socketRef = useRef(null);
  const [eventPayload, setEventPayload] = useState();
  const [actionEventPayload, setActionEventPayload] = useState();

  const handleActionEventPayload = useCallback((payload) => {
    if (payload) setActionEventPayload(payload);
  }, []);

  const handleEventPayload = useCallback((payload) => {
    if (payload) setEventPayload(payload);
  }, []);

  useEffect(() => {
    if (!gameId) return;

    let sock;

    const registerHandlers = () => {
      // Primero eliminamos cualquier handler previo
      sock.off("card_played_event", handleEventPayload);
      sock.off("select_card", handleSelectCardPayload);
      sock.off("player_secrets", handleSecretsPayload);
      sock.off("action_event", handleActionEventPayload);
      sock.off("select_player", handleSelectPlayerPayload);
      sock.off("resolve_select_card_to_requester", handleSelectCardResolve);
      sock.off("resolve_select_player_to_requester", (payload) => {
        handleSelectPlayerResolve(payload, playerId);
      });

      sock.off("sfp_reveal_secret", handleDeviousCard);

      // Registramos handlers
      sock.on("card_played_event", handleEventPayload);
      sock.on("select_card", handleSelectCardPayload);
      sock.on("select_player", handleSelectPlayerPayload);
      sock.on("action_event", handleActionEventPayload);
      sock.on("player_secrets", handleSecretsPayload);
      sock.on("resolve_select_card_to_requester", handleSelectCardResolve);
      sock.on("resolve_select_player_to_requester", (payload) => {
        handleSelectPlayerResolve(payload, playerId);
      });

      // Devious
      sock.on("sfp_reveal_secret", (payload) => {
        handleDeviousCard(payload, playerId);
      });
    };

    const connect = async () => {
      try {
        sock = await getSocket();
        socketRef.current = sock;

        if (sock.connected) {
          registerHandlers();
        } else {
          sock.on("connect", registerHandlers);
        }
      } catch (err) {
        console.error(
          "Socket connection in initWebSocketListeners failed:",
          err
        );
      }
    };

    connect();

    return () => {
      if (sock) {
        sock.off("card_played_event", handleEventPayload);
        sock.off("select_card", handleSelectCardPayload);
        sock.off("player_secrets", handleSecretsPayload);
        sock.off("resolve_select_card_to_requester", handleSelectCardResolve);
        sock.off("action_event", handleActionEventPayload);
        sock.off("resolve_select_player_to_requester", (payload) => {
          handleSelectPlayerResolve(payload, playerId);
        });
        sock.off("select_player", handleSelectPlayerPayload);
        sock.off("sfp_reveal_secret", handleDeviousCard);
      }
    };
  }, [gameId]);

  return {
    eventPayload,
    actionEventPayload,
  };
}
