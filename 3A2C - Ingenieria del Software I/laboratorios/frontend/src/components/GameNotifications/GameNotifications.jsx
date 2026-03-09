import useGameNotification from "../../containers/Game/GameNotificationsContainer";
import { useNavigate } from "react-router-dom";
import useGameInfo from "../../containers/Game/GameInfoContainer";

export default function GameNotifications({ gameId }) {
  const { gameNotification } = useGameNotification(gameId);
  const { gameInfo } = useGameInfo(gameId);
  const navigate = useNavigate();

  if (!gameNotification) return null;

  const handleClick = () => {
    navigate("/");
  };

  const getPlayerName = (playerId) => {
    if (!gameInfo || !gameInfo.players) return playerId;
    const player = gameInfo.players.find((j) => j.player_id === playerId);
    return player ? player.name : playerId;
  };

  const getNonMurderers = () => {
    if (!gameInfo || !gameInfo.players || !gameNotification.payload.target_id)
      return [];
    return gameInfo.players.filter(
      (j) => String(j.player_id) !== String(gameNotification.payload.target_id)
    );
  };

  const isEscapeVictory =
    gameNotification.payload.reason === "The murderer escapes";
  const isRevealVictory =
    gameNotification.payload.reason === "The murderer has been revealed";

  return (
    <div className="absolute inset-0 flex items-center justify-center pointer-events-auto z-50">
      {/* Transparent overlay */}
      <div className="absolute inset-0 bg-black/60"></div>

      <div
        className="relative w-full max-w-[1500px] p-8 rounded-lg bg-slate-900 shadow-[0_0_4px_#c2a22d] 
                hover:shadow-[0_0_8px_#c2a22d] transition-shadow duration-100 ease-in-out flex flex-col items-center"
      >
        <p className="tracking-wide font-metamorphous text-center text-lg text-[#c2a22d] mb-2">
          Agatha Christie's
        </p>

        <h2 className="tracking-wide font-metamorphous text-center text-5xl text-white mb-8">
          Death on the Cards
        </h2>

        <h2 className="tracking-wide font-metamorphous text-center text-6xl text-white font-bold mb-8">
          {gameNotification.payload.reason}
        </h2>

        {isEscapeVictory && (
          <h3 className="tracking-wide font-metamorphous text-center text-3xl text-white mb-8">
            Winner: {getPlayerName(gameNotification.payload.winner_id)}
          </h3>
        )}

        {isRevealVictory && (
          <>
            <h3 className="tracking-wide font-metamorphous text-center text-3xl text-white mb-4">
              The murderer was revealed by:{" "}
              {getPlayerName(gameNotification.payload.actor_id)}
            </h3>
            <h4 className="tracking-wide font-metamorphous text-center text-xl text-[#c2a22d] mb-2">
              The murderer was:{" "}
              {getPlayerName(gameNotification.payload.target_id)}
            </h4>
            <h4 className="tracking-wide font-metamorphous text-center text-xl text-[#c2a22d] mb-4">
              The rest of the players win!
            </h4>
            <ul className="text-white text-lg font-metamorphous mb-8">
              {getNonMurderers().map((j) => (
                <li key={j.player_id}>{j.name}</li>
              ))}
            </ul>
          </>
        )}

        {(isEscapeVictory || isRevealVictory) && (
          <button
            type="submit"
            className="font-metamorphous text-center px-20 py-5 rounded-xl focus:outline-none mb-4"
            style={{ background: "#0b3b6f", color: "white" }}
            onClick={handleClick}
            onMouseOver={(e) => {
              e.currentTarget.style.background = "#c2a22d";
              e.currentTarget.style.color = "black";
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.background = "#0b3b6f";
              e.currentTarget.style.color = "white";
            }}
          >
            Exit
          </button>
        )}

        <div className="-mx-8 -my-8 absolute bottom-0 left-0 box-border size-15 shadow-[-3px_3px_1px_#c2a22d] rounded-2xl"></div>
        <div className="-mx-8 -my-8 absolute right-0 bottom-0 box-border size-15 shadow-[3px_3px_1px_#c2a22d] rounded-2xl"></div>
        <div className="-mx-8 -my-8 absolute top-0 right-0 box-border size-15 shadow-[3px_-3px_1px_#c2a22d] rounded-2xl"></div>
        <div className="-mx-8 -my-8 absolute top-0 left-0 box-border size-15 shadow-[-3px_-3px_1px_#c2a22d] rounded-2xl"></div>
      </div>
    </div>
  );
}
