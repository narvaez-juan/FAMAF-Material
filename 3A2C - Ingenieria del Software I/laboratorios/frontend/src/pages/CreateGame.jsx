import GameForm from "../components/GameForm/GameForm";
import { createHttpService } from "../services/HTTPServices";
import { useState } from "react";
import getSocket from "../services/WSServices";
import { useNavigate } from "react-router-dom";

export default function CreateGame() {
  const [httpService] = useState(() => createHttpService());
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleCreateGame = async (gameData) => {

    setError('');

    try {
      const response = await httpService.createGame(gameData);
      console.log("Server response:", response)

      // Save the new room ID in localStorage
      localStorage.setItem("RoomID", response.game_id);

      // Connect to the new game's room
      const sock = await getSocket();
      sock.emit("join_game", `game:${response.game_id}`);
      console.log("Joined room:", `game:${response.game_id}`);

      // Go to lobby
      navigate(`/games/${response.game_id}/lobbies`, {
        state: { playerId: response.player_id }
      });

    } catch (error) {
      if (error.status == 409) {
        setError("Game name already in use, please choose another one")
      } else {
        setError("Something went wrong, please try again")
      }

      throw error;
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950">
      
      <div className="w-full max-w-2xl p-8 rounded-lg shadow-2xl bg-slate-900">
        <h1 className="text-2xl font-semibold text-white mb-4">Create a New Game</h1>
        <p className="text-sm text-blue-100/70 mb-6">Fill out the details below to create a new game session.</p>
        <GameForm onSubmit={handleCreateGame} onChange={() => SetError(false)}/>
        {error && <p className="mt-1 text-sm text-red-600 dark:text-red-400">{error}</p>}
      </div>
    </div>
  );
}