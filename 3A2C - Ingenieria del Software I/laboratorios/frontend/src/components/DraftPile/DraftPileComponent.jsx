import Card from "../Card/Card";

export default function DraftPileComponent({
  loading,
  draftPile,
  handleCardClick,
  selectedCards,
}) {
  return (
    <div className="flex items-end justify-center gap-12 mt-[-20px] h-52">
      {draftPile && draftPile.length > 0 ? (
        draftPile.map((card) => {
          const stableKey = card.gameCardId ?? card.card_id ?? card.id;
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
              onClick={() => handleCardClick(stableKey)}
              isSelected={selectedCards.includes(stableKey)}
            />
          );
        })
      ) : !loading ? (
        <p className="text-white">No cards in draft pile.</p>
      ) : null}
    </div>
  );
}
