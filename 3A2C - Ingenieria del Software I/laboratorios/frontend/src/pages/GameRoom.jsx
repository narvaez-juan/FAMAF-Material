import GameTable from "../components/GameTable/GameTable";
import useGameRoomData from "../containers/Game/GameRoomContainer";
import useDiscardPile from "../containers/Deck/DiscardPileContainer";
import useDrawPile from "../containers/Deck/DrawPileContainer";
import StatusMessage from "../components/StatusMessage/StatusMessage";
import { useParams, useLocation } from "react-router-dom";
import GameNotifications from "../components/GameNotifications/GameNotifications";
import PlayerHandContainer from "../containers/PlayerHand/PlayerHandContainer";
import useSets from "../containers/GameLogic/PlaySetContainer";

export default function GameRoom() {
  const { state } = useLocation();
  const playerId = state?.playerId;

  const { gameId } = useParams(); //NOTE - Takes gameId from the URL in App.jsx
  const { jugadores, turnoActual, loading, error, enCurso } =
    useGameRoomData(gameId);
  const { discardPile } = useDiscardPile(gameId);
  const { drawPile } = useDrawPile(gameId);
  const { allSets } = useSets(gameId, playerId);

  if (loading) return <StatusMessage message="Loading game..." />;
  if (error) return <StatusMessage message={error} color="red" />;
  if (!enCurso)
    return (
      <StatusMessage message="The game has not started yet" color="yellow" />
    );

  return (
    <div className="relative min-h-screen w-full bg-slate-950 text-white overflow-hidden">
      {/* Círculo al fondo */}

      <div
        className="absolute bottom-0 left-1/2 -translate-x-1/2
     w-[110vw] h-[150vw] max-w-[2000px] max-h-[2000px]
     rounded-full
     bg-[radial-gradient(circle_at_center,_#a43823_0%,_#5c1f14_80%,_#2b0d08_100%)]
     border-8 border-[#421a12] z-0"
      />

      {/* Contenido por encima */}
      <div className="relative z-10">
        <GameNotifications gameId={gameId} className="relative z-50" />
        <GameTable
          jugadores={jugadores}
          turnoActual={turnoActual}
          discardPile={discardPile}
          drawPile={drawPile}
          playerId={playerId}
          gameId={gameId}
          PlayerHandContainer={PlayerHandContainer}
          allSets={allSets}
        />
      </div>
    </div>
  );
}
