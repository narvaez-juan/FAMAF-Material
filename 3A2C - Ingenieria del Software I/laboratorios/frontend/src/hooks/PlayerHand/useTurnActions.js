import { useState, useRef, useCallback } from "react";
import useCountDown from "../Timer/useCountDown";
import { useEffect } from "react";
import { useEventCardStore } from "../../Store/useEventCardStore";
import { getEventCardHandler } from "../../hooks/Card/EventCard/CardsHandlerFactory.jsx";

export default function useTurnActions({
  gameId,
  playerId,
  playerHand,
  selectedCards,
  setSelectedCards,
  selectedDraftCards,
  setSelectedDraftCards,
  selectedDrawCardsNumber,
  setSelectedDrawCardsNumber,
  httpService,
  drawCard,
  finishTurn,
  isMyTurn,
  finishLoading,
  setDiscardedCount,
  playersNumber,
}) {
  // Guard for turn actions: "idle" | "discarded" | "finishing" | "stealing"
  const [turnAction, setTurnAction] = useState("idle");
  const [playerHasDiscarded, setHasDiscarded] = useState(false);
  //const [playerHasPlayedEvent, setPlayerHasPlayedEvent] = useState(false);

  // Event cards:
  const [onEventCardClick, setOnEventCardClick] = useState(false);
  const {
    setEventCardClicked,
    clearEventCardClicked,
    setPlayerHasPlayedEvent,
    playerHasPlayedEvent,
  } = useEventCardStore.getState();

  const eventCards = [
    "17-event_cardsonthetable.png",
    "18-event_anothervictim.png",
    "19-event_deadcardfolly.png",
    "20-event_lookashes.png",
    "21-event_cardtrade.png",
    "22-event_onemore.png",
    "23-event_delayescape.png",
    "24-event_earlytrain.png",
    "25-event_pointsuspicions.png",
  ];

  // Timer
  const TIMER_KEY = `SecondsLeft_${playerId}`;
  const { secondsLeft, start, stop, reset } = useCountDown(TIMER_KEY, 60);

  // Use a ref for any transient action context to avoid races
  const actionRef = useRef(null);

  // Turn logic
  useEffect(() => {
    if (isMyTurn) {
      start();
      setHasDiscarded(false);
      setPlayerHasPlayedEvent(false);
      setTurnAction("idle");
    } else {
      setSelectedCards([]);
      setTurnAction("idle");
    }
  }, [isMyTurn]);

  const handlePlayEventClick = async () => {
    // Always only one card
    const card = selectedCards[0];
    if (!card) return;

    // Get correct handler
    const handler = getEventCardHandler(card.name);
    if (!handler) return;

    const handLengthAfterPlay = playerHand.length - 1;
    const requiredDraws = Math.max(0, 6 - handLengthAfterPlay); // Nunca menos de 0

    try {
      await handler(card, { gameId, playerId, playersNumber });

      setPlayerHasPlayedEvent(true);
      setTurnAction("played_event_card");
      setSelectedCards([]);

      setDiscardedCount(requiredDraws);
    } catch (err) {
      console.error("Error playing event card:", err);
    }
  };

  const handleDiscardCard = useCallback(async () => {
    if (!isMyTurn || playerHasDiscarded || !selectedCards?.length) return;

    const cardsToDiscard = selectedCards.length;
    // Longitud inicial - N cartas descartadas (si ya jugó evento, ya se actualizó el déficit,solo sumamos)
    const handLengthAfterDiscard = playerHand.length - cardsToDiscard;
    const requiredDraws = Math.max(0, 6 - handLengthAfterDiscard);

    try {
      setTurnAction("discarded");
      if (typeof setDiscardedCount === "function")
        setDiscardedCount(requiredDraws);
      actionRef.current = { type: "discard" };
      const selectedIds = selectedCards.map((c) => c.id);
      await httpService.discardCard(gameId, playerId, selectedIds);
      setHasDiscarded(true);
      setSelectedCards([]);
    } catch (error) {
      console.error("Error discarding card:", error);
      setTurnAction("idle");
    } finally {
      actionRef.current = null;
    }
  }, [
    isMyTurn,
    playerHasDiscarded,
    selectedCards,
    httpService,
    gameId,
    playerId,
    setDiscardedCount,
    setSelectedCards,
  ]);

  const handleDrawCardClick = useCallback(async () => {
    try {
      await drawCard(
        gameId,
        playerId,
        selectedDraftCards,
        selectedDrawCardsNumber
      );
      if (typeof setSelectedDraftCards === "function")
        setSelectedDraftCards([]);
      if (typeof setSelectedDrawCardsNumber === "function") {
        setSelectedDrawCardsNumber(0);
        setDiscardedCount(0);
      }
    } catch (error) {
      console.error("Error drawing card:", error);
    }
  }, [
    drawCard,
    gameId,
    playerId,
    selectedDraftCards,
    selectedDrawCardsNumber,
    setSelectedDraftCards,
    setSelectedDrawCardsNumber,
  ]);

  const handleFinishClick = useCallback(async () => {
    if (!isMyTurn || finishLoading) return;
    try {
      setTurnAction("finishing");
      let cardsToDrawFromDeck = 6 - (playerHand?.length || 0);
      await finishTurn(
        gameId,
        playerId,
        playerHasDiscarded,
        playerHasPlayedEvent,
        playerHand,
        cardsToDrawFromDeck
      );
    } catch (err) {
      console.error("Error finishing turn:", err);
      setTurnAction("idle");
    }
    // Stop and reset timer
    stop();
    reset();

    setPlayerHasPlayedEvent(false);
    setHasDiscarded(false);
    setDiscardedCount(0);
  }, [
    isMyTurn,
    finishLoading,
    finishTurn,
    gameId,
    playerId,
    playerHasDiscarded,
    playerHand,
  ]);

  const handleCardClick = useCallback(
    (gameCardId, gameCardName) => {
      if (!isMyTurn || playerHasDiscarded || turnAction === "finishing") {
        return;
      }
      setSelectedCards((prev) => {
        const newSelection = prev.some((c) => c.id === gameCardId)
          ? prev.filter((c) => c.id !== gameCardId)
          : [...prev, { id: gameCardId, name: gameCardName }];

        // Play Card Button
        if (
          !playerHasPlayedEvent &&
          newSelection.length === 1 &&
          eventCards.includes(gameCardName)
        ) {
          setOnEventCardClick(true);
          const eventCard = newSelection[0];

          // Handle onemore event
          let effect;
          if (eventCard.name === "22-event_onemore.png") {
            effect = "OneMore";
          } else {
            effect = "EventCard";
          }
          setEventCardClicked({
            id: eventCard.id,
            name: eventCard.name,
            effect,
          });
        } else {
          setOnEventCardClick(false);
          clearEventCardClicked();
        }

        return newSelection;
      });
    },
    [
      isMyTurn,
      playerHasDiscarded,
      turnAction,
      setSelectedCards,
      selectedCards,
      eventCards,
    ]
  );

  useEffect(() => {
    if (secondsLeft === 0) {
      handleFinishClick();
    }
  }, [secondsLeft, handleFinishClick]);

  const isDiscardDisabled =
    !selectedCards ||
    selectedCards.length === 0 ||
    playerHasDiscarded ||
    !isMyTurn ||
    turnAction === "finishing" ||
    turnAction === "discarded";

  const isFinishDisabled =
    finishLoading || !isMyTurn || turnAction === "finishing";

  const isDrawDisable =
    !isMyTurn || (!playerHasDiscarded && !playerHasPlayedEvent);

  return {
    handlePlayEventClick,
    handleDiscardCard,
    handleDrawCardClick,
    handleFinishClick,
    handleCardClick,
    isDiscardDisabled,
    isFinishDisabled,
    isDrawDisable,
    turnAction,
    setTurnAction,
    playerHasDiscarded,
    setHasDiscarded,
    secondsLeft,
    onEventCardClick,
  };
}
