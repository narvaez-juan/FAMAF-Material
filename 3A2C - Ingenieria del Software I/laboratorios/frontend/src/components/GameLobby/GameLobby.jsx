import PlayerCard from "../PlayerCard/PlayerCard";
import StartGame from "../StartGame/StartGame";
export const GameLobby = ({ game, players = [], gameReady, playerId }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950">
      <div
        className="overflow-y-auto flex flex-col w-[1200px] h-[900px] shadow-[0_0_4px_#c2a22d] 
                p-10 rounded-lg bg-slate-900"
      >
        <h2
          className="tracking-wide font-metamorphous text-center 
                text-5xl text-white mb-6"
        >
          {game ? game.name : "Cargando partida..."}
        </h2>

        <div className="grid grid-cols-1 gap-4 max-w-[500px]">
          <h1
            className="tracking-wide font-metamorphous text-left 
                    text-2xl text-white mb-6"
          >
            Players in lobby: {players.length} / {game?.maxPlayers ?? "-"}
          </h1>

          <ul className="space-y-6">
            {players.map((player) => (
              <li key={player.name}>
                <PlayerCard PlayerName={player.name} />
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-auto">
          <StartGame game={game} gameReady={gameReady} playerId={playerId} />
        </div>
      </div>
    </div>
  );
};
