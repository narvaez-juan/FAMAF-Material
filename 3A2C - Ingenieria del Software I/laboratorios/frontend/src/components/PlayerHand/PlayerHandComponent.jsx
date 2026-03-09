import ButtonGrid from "../ButtonGrid/ButtonGrid";
import Card from "../Card/Card";

export default function PlayerHandComponent({
  loading,
  playerHand,
  selectedCards,
  isDiscardDisabled,
  isFinishDisabled,
  finishLoading,
  finishError,
  onDiscardCard,
  onFinishClick,
  onCardClick,
  onDrawClick,
  onPlaySetClick,
  isDrawDisable,
  secondsLeft,
  isMyTurn,
  onEventCardClick,
  onPlayEventClick,
}) {
  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-4">
        <div className="text-white"></div>
        {/* Botones */}
        <div>
          <ButtonGrid
            buttons={[
              {
                buttonColor: "#8b2e2e",
                buttonHoverColor: "#c2322d",
                onDisabledHandler: isDiscardDisabled,
                onClickHandler: onDiscardCard,
                buttonText: `Discard (${selectedCards.length})`,
                buttonActive: true,
              },
              {
                buttonColor: "#0b3b6f",
                buttonHoverColor: "#c2a22d",
                onDisabledHandler: isFinishDisabled,
                onClickHandler: onFinishClick,
                buttonText: finishLoading
                  ? "Loading..."
                  : `End Turn(${isMyTurn ? secondsLeft : 60})`,
                buttonActive: true,
              },
              {
                buttonColor: "#0b3b6f",
                buttonHoverColor: "#c2a22d",
                onDisabledHandler: isDrawDisable,
                onClickHandler: onDrawClick,
                buttonText: "Draw Card",
                buttonActive: true,
              },
              {
                buttonColor: "#0b3b6f",
                buttonHoverColor: "#c2a22d",
                onDisabledHandler: selectedCards.length === 0,
                onClickHandler: onPlaySetClick,
                buttonText: `Play Set (${selectedCards.length})`,
                buttonActive: true,
              },
              {
                buttonColor: "#0b3b6f",
                buttonHoverColor: "#c2a22d",
                onClickHandler: onPlayEventClick,
                buttonText: "Play Card",
                buttonActive: onEventCardClick,
              },
            ]}
          ></ButtonGrid>

          {finishError && (
            <div className="text-red-300 ml-4">{finishError}</div>
          )}
        </div>
      </div>

      <div className="relative flex justify-center items-end w-full h-48">
        {playerHand.length > 0 ? (
          playerHand.map((card, index) => {
            const stableKey = card.gameCardId ?? card.card_id;
            const total = playerHand.length;
            const rotation = (index - (total - 1) / 2) * 12;
            const translateY = Math.abs(index - (total - 1) / 2) * 7;
            const spacing = 50; // distancia entre cartas

            if (!stableKey) {
              console.error(
                "Card object is missing a unique key (gameCardId or card_id):",
                card
              );
              return null;
            }

            return (
              <div
                key={stableKey}
                className="absolute"
                style={{
                  transform: `rotate(${rotation}deg) translateY(${translateY}px)`,
                  transformOrigin: "bottom center",
                  left: `calc(50% - ${((total - 1) * spacing) / 2}px + ${
                    index * spacing
                  }px)`,
                }}
              >
                <Card
                  image={card.image}
                  alt={`Card ${stableKey}`}
                  onClick={() => onCardClick(stableKey, card.image)}
                  isSelected={selectedCards.some((c) => c.id === stableKey)}
                  size="w-28 h-38"
                />
              </div>
            );
          })
        ) : (
          <p className="font-metamorphous text-white h-12">
            You don't have cards in your hand.
          </p>
        )}
      </div>
    </div>
  );
}
