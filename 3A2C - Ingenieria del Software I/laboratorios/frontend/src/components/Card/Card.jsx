const Card = ({
  image,
  alt = "card",
  onClick,
  isSelected = false,
  isDisabled = false,
  showPlaceholder = false,
  size = "w-20 h-28",
}) => {
  // Manejar imagen no disponible
  const cardImage = (() => {
    if (!image) return null;
    const trimmed = image.trim();
    if (trimmed.startsWith("http") || trimmed.startsWith("/")) {
      return trimmed;
    }
    return `/Cartas/${trimmed}`;
  })();

  return (
    <div
      className={`
    relative ${size} rounded-xl overflow-hidden flex
    transition-all duration-200
    ${!isDisabled && "hover:scale-105 hover:-translate-y-1 cursor-pointer"}
    ${isSelected && "ring-2 ring-yellow-500"} 
    ${isDisabled && "opacity-50 cursor-not-allowed"}
    ${showPlaceholder && "border-2 border-dashed border-gray-400 bg-gray-100"}
  `}
      onClick={!isDisabled ? onClick : undefined}
      role="button"
      tabIndex={!isDisabled ? 0 : -1}
      onKeyDown={(e) => {
        if (!isDisabled && (e.key === "Enter" || e.key === " ")) {
          e.preventDefault();
          onClick?.();
        }
      }}
    >
      {!showPlaceholder ? (
        <>
          <img
            src={cardImage || "/Cartas/00-help.png"}
            alt={alt}
            className={"object-cover select-none w-full h-full"}
            draggable={false}
            onError={(e) => {
              // Fallback si la imagen no carga
              e.target.src = "/Cartas/00-help.png";
            }}
          />
        </>
      ) : (
        <div className="w-full h-full flex items-center justify-center text-gray-400">
          <span className="text-4xl">+</span>
        </div>
      )}
    </div>
  );
};

export default Card;
