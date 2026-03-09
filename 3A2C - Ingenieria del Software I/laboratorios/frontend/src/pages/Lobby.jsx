import { useParams, useLocation } from "react-router-dom";
import { GameLobby } from "../components/GameLobby/GameLobby";
import { useState, useEffect } from "react";
import getSocket from "../services/WSServices";
import { useNavigate } from "react-router-dom";

export default function Lobby() {
  const [game, setGame] = useState(null);
  const [players, setPlayers] = useState([]);
  const [gameReady, setGameReady] = useState(false);

  const { gameId } = useParams();
  const { state } = useLocation();
  const playerId = state?.playerId;

  const navigate = useNavigate();

  useEffect(() => {
    let sock;
    let mounted = true;

    const onGameInfo = (gameInfo) => {
      console.log("[lobby] game_info", gameInfo);
      if (!mounted) return;
      setGame(gameInfo);
      setPlayers(gameInfo.players || []);
      setGameReady(gameInfo.currentPlayers >= gameInfo.minPlayers);
    };
    const onPlayerJoined = (player) => {
      console.log("[lobby] player_joined", player);
      if (!mounted) return;
      setPlayers((prev) => [...prev, { name: player.playerName }]);
    };

    const onGameStarted = (payload) => {
      console.log(
        "[lobby] game_started received",
        payload,
        "socket id:",
        sock?.id
      );
      // navegación basada en servidor
      navigate(`/games/${payload.id}`, {
        state: { playerId: playerId },
      });
    };

    const onInitialDraftPile = (payload) => {
      localStorage.setItem("draft_piles", JSON.stringify(payload));
    };

    const onInitialHand = (payload) => {
      localStorage.setItem("initialHand", JSON.stringify(payload));
      console.log("PlayerHand Received");
    };

    const onInitialSecrets = (payload) => {
      localStorage.setItem("initialSecrets", JSON.stringify(payload));
      console.log("PlayerSecrets Received");
    };

    const connect = async () => {
      // Save RoomID
      if (!localStorage.getItem("RoomID")) {
        localStorage.setItem("RoomID", gameId);
      }

      sock = await getSocket();

      // Request enter the room
      sock.emit("join_game", gameId);

      // Request game info
      sock.emit("get_game_info", gameId);

      sock.on("game_info", onGameInfo);
      sock.on("player_joined", onPlayerJoined);
      sock.on("game_started", onGameStarted);
      sock.on("initial_hand", onInitialHand);
      sock.on("initial_secrets", onInitialSecrets);
      sock.on("draft_piles", onInitialDraftPile);
    };

    connect();
  }, [gameId, navigate]);

  return (
    <GameLobby
      game={game}
      players={players}
      gameReady={gameReady}
      playerId={playerId}
    />
  );
}
