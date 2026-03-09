import { useEffect, useState } from "react";
import getSocket from "../../services/WSServices";

export default function useGameInfo(gameId) {
  const [gameInfo, setGameInfo] = useState();

  const handlePayload = (payload) => {
    if (payload) {
      setGameInfo(payload);
    }
  };

  useEffect(() => {
    const connect = async () => {
      try {
        const sock = await getSocket();

        sock.on("game_info", handlePayload);

        if (sock.connected) {
          sock.emit("get_game_info", gameId);
        } else {
          sock.on("connect", () => {
            sock.emit("get_game_info", gameId);
          });
        }
      } catch (err) {
        console.error("Socket connection in GameInfoContainer failed:", err);
      }
    };

    connect();
  }, [gameId]);

  return { gameInfo };
}
