import { useState, useMemo, useEffect } from "react";
import Card from "../Card/Card";
import { useEventCardStore } from "../../Store/useEventCardStore";
import { useDeadCardFollyStore } from "../../Store/DeadCardFollyStore";
import { resolveSelectCard } from "../../websocket/emitters/CardEmitter";

export default function SelectCardModal({
  cards,
  players,
  playerId,
  gameId,
  eventSelectedCard,
}) {
  const [selectedCard, setSelectedCard] = useState(null);
  const { selectCardInfo, setSelectCard } = useDeadCardFollyStore();
  const [secondsLeft, setSecondsLeft] = useState(10);

  // if player does not select a card in five seconds, get a random one
  useEffect(() => {
    const interval = setInterval(() => {
      setSecondsLeft((prev) => Math.max(prev - 1, 0));
    }, 1000);

    const timer = setTimeout(() => {
      const randomCard = cards[Math.floor(Math.random() * cards.length)];
      setSelectCard({ id: randomCard.gameCardId, image: randomCard.image });
      handleConfirm(randomCard);
    }, 10000);

    return () => {
      clearInterval(interval);
      clearTimeout(timer);
    };
  }, []);

  const handleCardClick = (id, image) => {
    if (eventSelectedCard && id === eventSelectedCard[0]?.id) return;
    setSelectedCard({ id, image });
  };

  // confirm card
  const handleConfirm = (randomCard = selectedCard) => {
    resolveSelectCard(
      gameId,
      playerId,
      selectedCard?.id || randomCard?.gameCardId,
      selectedCard?.image || randomCard?.image,
      selectCardInfo.player_id
    );
    setSelectCard(false);
  };

  const infoText = useMemo(() => {
    if (!selectCardInfo || !players) return "";

    const { player_id, direction, card_name } = selectCardInfo;

    const requester = players.find((p) => p.id_jugador === player_id);
    const requesterName = requester?.nombre || "Unknown";

    if (player_id === playerId) {
      // Im the one who played the card
      return `Select a card from your hand to pass to the player on your ${direction}. ${secondsLeft}`;
    } else {
      // Another played the card
      return `${requesterName} played the event card "${card_name}". You must select a card to pass to the player on your ${direction}. ${secondsLeft}`;
    }
  }, [selectCardInfo, players, playerId, secondsLeft]);

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-40 flex items-center justify-center">
      {/* main container */}
      <div className="relative bg-gray-900 rounded-2xl shadow-lg p-6 flex flex-col items-center">
        <h2 className="text-white text-xl font-metamorphous mb-2">
          Event Action
        </h2>
        {infoText && (
          <p className="text-gray-300 text-center font-metamorphous mb-4 px-6">
            {infoText}
          </p>
        )}

        <h2 className="text-white text-xl font-metamorphous mb-4">
          Select a Card
        </h2>

        <div
          className="flex justify-center items-end gap-4 mx-auto mb-6"
          style={{
            width: `${cards.length * 9}rem`,
            maxWidth: "90vw",
          }}
        >
          {cards.length > 0 ? (
            cards.map((card) => {
              const stableKey = card.gameCardId ?? card.card_id;
              if (!stableKey) {
                console.error(
                  "Card object is missing a unique key (gameCardId or card_id):",
                  card
                );
                return null;
              }

              return (
                <Card
                  key={stableKey}
                  image={card.image}
                  alt={`Card ${stableKey}`}
                  onClick={() => handleCardClick(stableKey, card.image)}
                  isSelected={selectedCard?.id === stableKey}
                  size="w-38 h-48"
                />
              );
            })
          ) : (
            <p className="font-metamorphous text-white h-12">
              You don't have cards in your hand.
            </p>
          )}
        </div>

        {/* Confirm button */}
        <button
          onClick={handleConfirm}
          disabled={
            !selectedCard ||
            (eventSelectedCard && selectedCard.id === eventSelectedCard[0]?.id)
          }
          className={`inline-flex items-center justify-center rounded-xl px-6 py-2 text-sm font-metamorphous font-semibold shadow-[0_0_6px_#c2a22d] transition-all
            ${
              selectedCard
                ? "bg-[#c2a22d] text-black hover:brightness-95"
                : "bg-gray-700 text-gray-400 cursor-not-allowed"
            }`}
        >
          Confirm
        </button>
      </div>
    </div>
  );
}
