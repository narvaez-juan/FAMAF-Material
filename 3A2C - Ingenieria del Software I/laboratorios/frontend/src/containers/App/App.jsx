import { BrowserRouter, Routes, Route } from "react-router-dom";
import CreateGame from "../../pages/CreateGame";
import HomePage from "../../pages/HomePage";
import GameList from "../../pages/GameList";
import GameRoom from "../../pages/GameRoom";
import Lobby from "../../pages/Lobby";
import JoinGame from "../../pages/JoinGame";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/games/create" element={<CreateGame />} />
          <Route path="/games/list" element={<GameList />} />
          <Route path="/games/:gameId" element={<GameRoom />} />
          <Route path="/games/:gameId/lobbies" element={<Lobby />} />
          <Route path="/games/:gameId/join/" element={<JoinGame />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
