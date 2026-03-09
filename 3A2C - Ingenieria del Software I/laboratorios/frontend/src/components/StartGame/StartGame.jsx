import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createHttpService } from "../../services/HTTPServices";

//NOTE - game has the format of the event game_info emmited by the backend
export default function StartGame({ game, gameReady, playerId }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [httpService] = useState(() => createHttpService());

  const isGameCreator = game?.players?.[0]?.player_id === playerId;

  const handleStart = async () => {
    if (!game?.id) {
      setError("Invalid gameId");
      return;
    }

    setError("");
    setLoading(true);

    try {
      //NOTE - This makes anyplayer on the lobby capable of starting the game
      console.log("Jugador que inicia la partida", game.players[0].player_id);

      console.log("Id de la partida que le paso al startGame", game.id);
      const response = await httpService.startGame(
        game.id,
        game.players[0].player_id
      );
      console.log("Server Response to startGame: ", response);
    } catch (error) {
      if (error?.status === 401) {
        setError("You dont have permission to start the dame");
      }
      //NOTE - This error should never happend due to the logic of the lobby
      else if (error.status === 406) {
        setError("The minimum number of players is not met");
      } else {
        console.error("StartGame error:", error);
        const status = error?.status ?? error?.response?.status;
        const serverMsg =
          error?.body?.detail ??
          error?.body?.message ??
          error?.response?.data ??
          error?.message;
        const detailForDev =
          process.env.NODE_ENV === "development"
            ? ` — ${JSON.stringify(
                error?.body ?? error?.response?.data ?? error?.message
              )}`
            : "";
        if (status === 401)
          setError(
            "You don't have permission to start the game" + detailForDev
          );
        else if (status === 406)
          setError("The minimum number of players is not met" + detailForDev);
        else {
          setError(`Something went wrong on StartGame${detailForDev}`);
          console.log(error);
        }
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center mt-auto">
      {gameReady && isGameCreator && (
        <>
          <button
            type="button"
            onClick={handleStart}
            disabled={loading}
            aria-busy={loading}
            className={`font-metamorphous text-center px-20 py-5 m-10 rounded-xl focus:outline-none
                            ${
                              loading
                                ? "bg-gray-600 text-gray-200"
                                : "bg-[#0b3b6f] text-white hover:bg-[#c2a22d] hover:text-black"
                            }`}
          >
            {loading ? "Starting..." : "Start Game"}
          </button>
          {error && (
            <div className="text-red-400 mt-2" role="alert">
              {error}
            </div>
          )}
        </>
      )}
      {gameReady && !isGameCreator && (
        <div className="text-center py-5 m-10">
          <p className="font-metamorphous text-xl text-gray-400">
            Waiting for the host to start the game...
          </p>
        </div>
      )}
    </div>
  );
}
