import { useEffect, useState } from "react";
import getSocket from "../../services/WSServices";

export default function useDrawPile(gameId) {
  const [drawPile, setDrawPile] = useState();

  const handleHandPayload = (payload) => {
    if (payload) {
      setDrawPile(payload.deck_size);
    }
  };

  useEffect(() => {
    const connect = async () => {
      try {
        const sock = await getSocket();
        sock.emit("join_game", gameId);
        sock.on("draw_pile", handleHandPayload);

        // if already connected, request
        if (sock.connected) {
          sock.emit("get_draw_pile", gameId);
        } else {
          // if not, wait to connect
          sock.on("connect", () => {
            sock.emit("get_draw_pile", gameId);
          });
        }
      } catch (err) {
        console.error("Socket connection failed:", err);
      }
    };

    connect();
  }, [gameId]);

  return { drawPile };
}
