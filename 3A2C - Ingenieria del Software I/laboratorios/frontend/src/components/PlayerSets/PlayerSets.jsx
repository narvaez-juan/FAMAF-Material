import Card from "../Card/Card";

export default function PlayerSets({ sets }) {
  if (!sets || sets.length === 0) {
    return null;
  }

  const spacing = 15;
  const setWidth = 80;

  // Tomamos solo el último set
  const lastSet = sets.at(-1);

  if (!lastSet?.card_game_images?.length) {
    return null;
  }

  const total = lastSet.card_game_images.length;

  return (
    <div
      className="relative flex items-end"
      style={{ height: "120px", minWidth: `${setWidth}px` }}
    >
      <div
        className="relative flex justify-center items-end"
        style={{ height: "120px" }}
      >
        {lastSet.card_game_images.slice(0, 3).map((image, index) => {
          const rotation = (index - (total - 1) / 2) * 10;
          const translateY = Math.abs(index - (total - 1) / 2) * 2;
          const left = index * spacing - ((total - 1) * spacing) / 2;

          return (
            <div
              key={lastSet.card_game_ids[index]}
              className="absolute transition-transform duration-300 hover:scale-110"
              style={{
                transform: `rotate(${rotation}deg) translateY(${translateY}px)`,
                transformOrigin: "bottom center",
                left: `${left}px`,
              }}
            >
              <Card image={image} alt="SetCard" size="w-20 h-29" />
            </div>
          );
        })}
      </div>
    </div>
  );
}
