import DraftPileComponent from "../../components/DraftPile/DraftPileComponent";
import { useParams } from "react-router-dom";
import { useEffect, useState, useRef, useMemo } from "react";
import getSocket from "../../services/WSServices";
export default function DraftPileContainer({
  gameId,
  playerId,
  onSelectDraftCards,
  totalSelected,
  discardedCount,
}) {
  const [draftPile, setDraftPile] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCards, setSelectedCards] = useState([]);
  // NOTE - Sockets, servicios y hooks
  const socketRef = useRef(null);

  const { gameId: routeGameId } = useParams();
  const realGameId = gameId || routeGameId;

  const [currentTurnIndex, setCurrentTurnIndex] = useState(null);
  const [myPlayerIndex, setMyPlayerTurnNumber] = useState(null);

  const isMyTurn = useMemo(() => {
    const result =
      currentTurnIndex != null &&
      myPlayerIndex != null &&
      currentTurnIndex === myPlayerIndex;
    return result;
  }, [currentTurnIndex, myPlayerIndex]);

  const handleDraftPileInfo = (payload) => {
    try {
      if (payload && Array.isArray(payload.draft_cards)) {
        setDraftPile(payload.draft_cards);
        localStorage.setItem("draft_piles", JSON.stringify(payload));
      } else {
        console.log("Payload no válido para draft_piles:", payload);
        console.log("Payload no válido para draft_piles:", payload);
      }
    } catch (err) {
      console.log("Error handling Draft Pile info", err);
    }
  };

  const handleCardClick = (gameCardId) => {
    console.log("[handleCardClick] called with:", gameCardId);
    if (!isMyTurn) {
      console.log("[handleCardClick] blocked: not my turn");
      return;
    }

    if (
      totalSelected >= discardedCount &&
      !selectedCards.includes(gameCardId)
    ) {
      return;
    }
    console.log("[handleCardClick] called with:", gameCardId);
    if (!isMyTurn) {
      console.log("[handleCardClick] blocked: not my turn");
      return;
    }

    if (
      totalSelected >= discardedCount &&
      !selectedCards.includes(gameCardId)
    ) {
      return;
    }
    setSelectedCards((prev) => {
      let newSelected;
      if (prev.includes(gameCardId)) {
        newSelected = prev.filter((id) => id !== gameCardId);
        console.log(`[handleCardClick] Deseleccionada: ${gameCardId}`);
      } else {
        if (discardedCount == prev.length) {
          console.log(
            "[handleCardClick] blocked: límite alcanzado al seleccionar"
          );
          return prev;
        }
        newSelected = [...prev, gameCardId];
        console.log(`[handleCardClick] Seleccionada: ${gameCardId}`);
      }
      console.log("[handleCardClick] selectedCards:", newSelected);
      return newSelected;
    });
  };

  useEffect(() => {
    if (onSelectDraftCards) onSelectDraftCards(selectedCards);
  }, [selectedCards, onSelectDraftCards]);

  useEffect(() => {
    try {
      const savedDraftPile = localStorage.getItem("draft_piles");
      if (savedDraftPile) {
        try {
          const payload = JSON.parse(savedDraftPile);
          handleDraftPileInfo(payload);
        } catch (err) {
          console.log(
            "Error parsing handleDraftPileInfo from localstorage",
            err
          );
        }
      }
    } catch (error) {
      console.log("Error geting initial Draft Pile from localstorage", error);
    }
  }, []);

  //SECTION - useEffect to handle Websocket
  useEffect(() => {
    if (!realGameId || !playerId) return;

    let mounted = true;
    let onConnectNamed = null;

    const connectSocket = async () => {
      try {
        const sock = await getSocket();
        if (!socketRef.current) socketRef.current = sock;

        sock.on("game_info", handleGameInfo);
        sock.on("draft_piles", handleDraftPileInfo);

        onConnectNamed = () => {
          sock.emit("get_game_info", realGameId, (ack) => {
            if (ack) handleGameInfo(ack);
          });
        };

        if (sock.connected) onConnectNamed();
        sock.on("connect", onConnectNamed);

        if (mounted) setLoading(false);
      } catch (err) {
        if (mounted) setLoading(false);
      }
    };

    connectSocket();

    return () => {
      mounted = false;
      const sock = socketRef.current;
      if (sock) {
        sock.off("game_info", handleGameInfo);
        sock.off("draft_state", handleDraftPileInfo);
        if (onConnectNamed) sock.off("connect", onConnectNamed);
      }
    };
  }, [realGameId, playerId]);
  //!SECTION

  //SECTION - handle para GameInfo
  const handleGameInfo = (payload) => {
    if (!payload || typeof payload !== "object") return;
    if (payload.currentTurn !== undefined) {
      setCurrentTurnIndex(payload.currentTurn);
    }
    if (Array.isArray(payload.players)) {
      const me = payload.players.find(
        (p) => String(p.player_id) === String(playerId)
      );
      if (me) {
        setMyPlayerTurnNumber(me.playerTurn);
      }
    }
  };
  //!SECTION
  useEffect(() => {}, [selectedCards]);

  useEffect(() => {}, [draftPile]);

  useEffect(() => {
    if (!isMyTurn) {
      setSelectedCards([]);
    }
  }, [isMyTurn]);

  return (
    <DraftPileComponent
      loading={loading}
      draftPile={draftPile}
      handleCardClick={handleCardClick}
      selectedCards={selectedCards}
      isMyTurn={isMyTurn}
    />
  );
}
