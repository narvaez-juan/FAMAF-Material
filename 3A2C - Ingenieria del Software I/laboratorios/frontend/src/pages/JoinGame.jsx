import { useState } from "react";
import PlayerForm from "../components/JoinGameForm/JoinGameForm";
import { useParams } from "react-router-dom"; // Importa useParams
import { useNavigate } from "react-router-dom";
import { createHttpService } from "../services/HTTPServices";

export default function JoinGame() {
    const { gameId: urlGameId } = useParams(); 
    const [gameId] = useState(urlGameId || ""); 
    const navigate = useNavigate();
    const [httpService] = useState(() => createHttpService());


  const handleSubmit = async (data, game_id) => {
    console.log("Data player submitted:", data);
    console.log("Game ID being used:", game_id);
    
    //NOTE - Check undefined game_id
    if (!game_id || game_id === "undefined") {
      alert("Error: Game ID is missing or invalid");
      return;
    }

    //NOTE - Convert to INT game_id
    const numericGameId = parseInt(game_id);
    if (isNaN(numericGameId)) {
      alert("Error: Game ID must be a valid number");
      return;
    }

    try {
      const responseData = await httpService.joinGame(
        data.player_name,
        data.player_birth_date,
        game_id
      );

      console.log("Success:", responseData);

      navigate(`/games/${numericGameId}/lobbies`, {
        state: { playerId: responseData.player_id }
      });

    } catch (error) {
      console.error("Error:", error);
      alert(`Error: ${error.message}`);
    }
  };

return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950">
        <div className="w-full max-w-3xl h-auto p-8 rounded-lg bg-slate-900 shadow-[0_0_4px_#c2a22d] relative">
            <p className="tracking-wide font-metamorphous text-center text-lg text-[#c2a22d] mb-2">Agatha Christie's</p>
            <h2 className="tracking-wide font-metamorphous text-center text-5xl text-white mb-4">Death on the Cards</h2>
            <h3 className="tracking-wide font-metamorphous text-center text-2xl text-white mb-4">
                Join Existing Game {urlGameId ? `- ID: ${urlGameId}` : ""} {/* //FIXME - Change game_id for game_name */}
            </h3>
            <p className="tracking-wide font-metamorphous text-center text-sm text-white mb-6">Fill out the details below to join the game session.</p>
            
            {/* //NOTE - PASS THE GAME ID HERE  */} 
            <PlayerForm onSubmit={handleSubmit} gameId={gameId} />

            <div className="-mx-8 -my-8 absolute bottom-0 left-0 box-border size-15 shadow-[-3px_3px_1px_#c2a22d] rounded-2xl"></div>
            <div className="-mx-8 -my-8 absolute right-0 bottom-0 box-border size-15 shadow-[3px_3px_1px_#c2a22d] rounded-2xl"></div>
            <div className="-mx-8 -my-8 absolute top-0 right-0 box-border size-15 shadow-[3px_-3px_1px_#c2a22d] rounded-2xl"></div>
            <div className="-mx-8 -my-8 absolute top-0 left-0 box-border size-15 shadow-[-3px_-3px_1px_#c2a22d] rounded-2xl"></div>
        </div>
    </div>
);
}