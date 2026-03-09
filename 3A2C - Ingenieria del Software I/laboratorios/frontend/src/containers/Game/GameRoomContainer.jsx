import { useEffect, useState, useRef } from "react";
import fetchPlayerInfo from "../PlayerInfo/PlayerInfoContainer";
import getSocket from "../../services/WSServices";

export default function useGameRoomData(gameId) {
  const [jugadores, setJugadores] = useState([]);
  const [turnoActual, setTurnoActual] = useState(null);
  const [enCurso, setEnCurso] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const socketRef = useRef(null);

  useEffect(() => {
    let mounted = true;

    const loadInitialData = async () => {
      try {
        const { jugadores, turnoActual, enCurso } = await fetchPlayerInfo(
          gameId
        );
        if (!mounted) return;
        setJugadores(jugadores);
        setTurnoActual(turnoActual);
        setEnCurso(enCurso);
      } catch (err) {
        if (!mounted) return;
        if (err.response?.status === 404) {
          setError("Game not found");
        } else if (err.status === 400) {
          setError("Invalid request");
        } else {
          setError("Unexpected error loading game");
        }
      } finally {
        if (mounted) setLoading(false);
      }
    };

    const initSocket = async () => {
      try {
        if (!localStorage.getItem("RoomID") && gameId) {
          localStorage.setItem("RoomID", gameId);
        }

        const sock = await getSocket();
        socketRef.current = sock;
        sock.emit("join_game", gameId);

        sock.on("turn_update", (payload) => {
          setTurnoActual(payload.turnoActual);
          setJugadores(payload.jugadores);
          setEnCurso(payload.enCurso);
        });
      } catch (err) {
        if (mounted) setError("WebSocket connection error");
      }
    };

    if (gameId) {
      loadInitialData();
      initSocket();
    }

    return () => {
      mounted = false;
      const sock = socketRef.current;
      if (sock) {
        sock.off("turn_update");
      }
    };
  }, [gameId]);

  return { jugadores, turnoActual, enCurso, loading, error };
}
