import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import GameCard from "../components/GameCard/GameCard";
import getSocket from "../services/WSServices";

export default function GameList() {
  const navigate = useNavigate();
  const { gameId } = useParams();
  const [games, setGames] = useState([]);

  const goToLobby = (gameId) => {
    navigate(`/games/${gameId}/join/`);
  };

  useEffect(() => {
    let sock;

    const connect = async () => {
      try {
        if (!localStorage.getItem("RoomID") && gameId) {
          localStorage.setItem("RoomID", gameId);
        }

        sock = await getSocket();
        sock.emit("join_game_list");

        sock.on("game_list", (gameList) => {
          console.log("List of games received:", gameList);
          setGames(Array.isArray(gameList) ? gameList : []);
        });
      } catch (err) {
        console.error("Socket connection failed:", err);
      }
    };

    connect();

    return () => {
      if (sock) {
        sock.off("game_list");
      }
    };
  }, [gameId]);

  return (
    <div className="min-h-screen bg-slate-950 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold text-blue-50 text-center mb-8 font-metamorphous">
          Game List
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 justify-items-center">
          {games.map((game) => (
            <GameCard
              key={game.id}
              gameName={game.name}
              currentPlayers={game.currentPlayers}
              maxPlayers={game.maxPlayers}
              onJoin={() => goToLobby(game.id)}
              aria-label={`Join ${game.name} (${game.currentPlayers}/${game.maxPlayers} players)`}
              role="button"
            />
          ))}
        </div>

        {games.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg font-metamorphous">
              No games available at the moment
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
