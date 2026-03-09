import GameMenu from "../components/GameMenu/GameMenu";

export default function HomePage() {

    return (
       <GameMenu createGameLink="/games/create" listGamesLink="/games/list" />
    );
}