import { useEffect, useState, useRef } from "react";
import getSocket from "../../services/WSServices";
import { useEventCardStore } from "../../Store/useEventCardStore";
import { delayMurderEscapesStore } from "../../Store/DelayMurderEscapesStore";
import { intoTheAshesStore } from "../../Store/IntoTheAshesStore";
import toast from "react-hot-toast";

export default function useDiscardPile(gameId) {
  const [discardPile, setDiscardPile] = useState([]);
  const [loading, setLoading] = useState(true);
  const socketRef = useRef(null);
  const [selectedCards, setSelectedCards] = useState([]);

  // Event card
  const { setPlayerHasPlayedEvent } = useEventCardStore.getState();

  // Delay murderer
  const openDiscardModal = delayMurderEscapesStore(
    (state) => state.openDiscardModal
  );
  const { setOpenDiscardModal, setAllDiscardCardSelected } =
    delayMurderEscapesStore.getState();

  // Into the ashes
  const openModalByIntoTheAshes = intoTheAshesStore(
    (state) => state.openModalByIntoTheAshes
  );

  const { setOpenModal, setSelectedCardToDraw } = intoTheAshesStore.getState();

  const handleCardClick = (id, image) => {
    setSelectedCards((prevSelected) => {
      // only one card if into the ashes
      if (openModalByIntoTheAshes) {
        return [{ id, image }];
      }

      if (prevSelected.some((card) => card.id === id)) {
        return prevSelected.filter((card) => card.id !== id);
      }

      return [...prevSelected, { id, image }];
    });
  };

  // Delay murderer
  const handleOnConfirm = () => {
    if (selectedCards.length === 0) {
      toast.error("No cards selected.");
      return;
    }

    const card_ids = selectedCards.map((card) => card.id);
    setAllDiscardCardSelected(card_ids);
    setSelectedCards([]);
  };

  // Into the Ashes
  const handleOnSelectAshesCard = () => {
    if (selectedCards.length !== 1) {
      toast.error("Must be one card.");
      return;
    }

    const card_id = selectedCards[0].id;
    setSelectedCardToDraw(card_id);
    setSelectedCards([]);
  };

  useEffect(() => {
    let mounted = true;

    const connect = async () => {
      try {
        if (!localStorage.getItem("RoomID") && gameId) {
          localStorage.setItem("RoomID", gameId);
        }

        const sock = await getSocket();
        socketRef.current = sock;
        sock.emit("join_game", gameId);

        sock.on("connect", () => {
          sock.emit("get_discard_pile", gameId);
        });

        sock.on("discard_pile", (payload) => {
          setDiscardPile(payload);
        });

        if (mounted) setLoading(false);
      } catch (err) {
        console.error("Socket connection failed:", err);
        if (mounted) setLoading(false);
      }
    };

    connect();

    return () => {
      mounted = false;
      const sock = socketRef.current;
      if (sock && typeof sock.off === "function") {
        // quitar listeners registrados
        sock.off("discard_pile");
        sock.off("connect");
      }
      socketRef.current = null;
    };
  }, [gameId]);

  return {
    discardPile,
    loading,
    openDiscardModal,
    setOpenDiscardModal,
    setPlayerHasPlayedEvent,
    handleCardClick,
    selectedCards,
    setSelectedCards,
    handleOnConfirm,
    openModalByIntoTheAshes,
    setOpenModal,
    handleOnSelectAshesCard,
  };
}
