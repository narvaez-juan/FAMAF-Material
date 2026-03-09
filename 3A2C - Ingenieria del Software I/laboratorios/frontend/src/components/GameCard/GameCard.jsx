export default function GameCard({
  gameName,
  currentPlayers,
  maxPlayers,
  onJoin,
}) {
  return (
    <div className="relative w-full max-w-[600px] h-[180px] p-8 rounded-lg bg-slate-900 shadow-[0_0_4px_#c2a22d] flex flex-col">
      <h2
        className="tracking-wide font-metamorphous text-left text-2xl text-white mb-6 overflow-hidden text-ellipsis whitespace-nowrap flex-shrink-0"
        title={gameName}
      >
        {gameName}
      </h2>

      <p className="font-metamorphous text-left text-white flex-shrink-0">
        Players: {currentPlayers}/{maxPlayers}
      </p>

      <button
        type="button"
        className="absolute bottom-6 right-6 font-metamorphous text-center px-4 py-3 text-white rounded-xl focus:outline-none transition-all duration-200"
        style={{ background: "#0b3b6f" }}
        onClick={onJoin}
        onMouseOver={(e) => {
          e.currentTarget.style.background = "#c2a22d";
          e.currentTarget.style.color = "black";
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.background = "#0b3b6f";
          e.currentTarget.style.color = "white";
        }}
      >
        Join Game
      </button>
    </div>
  );
}
