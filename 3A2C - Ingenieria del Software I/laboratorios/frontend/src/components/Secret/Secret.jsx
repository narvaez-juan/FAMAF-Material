const Secret = ({ image, alt = "Secret", isRevealed = false }) => {
  return (
    <div
      className={`
         w-36 h-56 rounded-xl overflow-hidden flex
        transition-all duration-200
        hover:scale-105 hover:-translate-y-2 cursor-pointer
      `}
    >
      {isRevealed ? (
        <>
          <img
            src={`/Cartas/${image}`}
            alt={alt}
            className="w-full h-full object-cover select-none"
            draggable={false}
            onError={(e) => {
              e.target.src = "/Cartas/00-help.png";
            }}
          />
        </>
      ) : (
        <>
          <img
            src={"/Cartas/05-secret_front.png"}
            alt={alt}
            className="w-full h-full object-cover select-none"
            draggable={false}
          />
        </>
      )}
    </div>
  );
};
export default Secret;
