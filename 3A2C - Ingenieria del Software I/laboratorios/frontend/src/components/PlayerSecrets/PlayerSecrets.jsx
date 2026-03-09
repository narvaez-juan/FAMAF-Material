import { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import Secret from "../Secret/Secret";
import getSocket from "../../services/WSServices";
import Button from "../Button/Button";

export default function PlayerSecret({ playerId }) {
  const { gameId } = useParams();
  const [playerSecrets, setPlayerSecrets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const socketRef = useRef(null);

  const handleSecretPayload = (payload) => {
    try {
      if (Array.isArray(payload)) {
        const player_secrets = payload.find((p) => p.player_id === playerId);
        if (player_secrets && Array.isArray(player_secrets.secrets_list)) {
          setPlayerSecrets(player_secrets.secrets_list);
        }
      } else {
        if (payload.player_id === playerId) {
          localStorage.removeItem("initialSecret");
          setPlayerSecrets(payload.secrets_list);
        }
      }
    } catch (error) {
      console.error("Error manejando payload de secretos:", error);
    }
  };

  // useEffect to read saved initial secrets from localStorage once
  useEffect(() => {
    const saved = localStorage.getItem("initialSecrets");
    if (saved) {
      try {
        const payload = JSON.parse(saved);
        handleSecretPayload(payload);
      } catch (err) {
        console.error("initialSecrets parse error:", err);
      }
    }
  }, []); // intencional: solo una vez al montar

  useEffect(() => {
    let mounted = true;

    const connect = async () => {
      try {
        if (!localStorage.getItem("RoomID") && gameId) {
          localStorage.setItem("RoomID", gameId);
        }

        const sock = await getSocket();
        socketRef.current = sock;

        const onConnect = () => {
          // pedir secretos al conectarse
          sock.emit("get_secrets", gameId, playerId);
        };

        // Registrar listeners
        sock.on("connect", onConnect);
        sock.on("initial_secrets", handleSecretPayload);
        sock.on("player_secrets", handleSecretPayload);

        if (mounted) setLoading(false);
      } catch (err) {
        console.error("Socket connection failed:", err);
        if (mounted) setLoading(false);
      }
    };

    connect();

    return () => {};
  }, [gameId, playerId]); // incluye playerId: si cambia, re-suscribimos

  return (
    <div>
      {/* Botón para abrir modal (estética GameMenu) */}
      <Button
        buttonColor={"#0b3b6f"}
        buttonHoverColor={"#c2a22d"}
        onClickHandler={() => setIsModalOpen(true)}
        buttonText={`Secrets`}
        className="fixed bottom-6 right-6 w-41 text-white"
      ></Button>

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div
            className="absolute inset-0 bg-black/80 backdrop-blur-sm"
            onClick={() => setIsModalOpen(false)}
          />

          <div className="relative w-full max-w-4xl max-h-[84vh] overflow-hidden rounded-2xl shadow-2xl border border-gray-700 z-50">
            <div className="bg-gradient-to-r from-blue-900 to-black px-6 py-5 border-b border-yellow-400">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-md bg-gradient-to-br from-[#112b57] to-[#0b3b6f] flex items-center justify-center shadow-[0_0_4px_#c2a22d]">
                    <span className="text-3xl font-metamorphous font-bold text-[#c2a22d]">
                      S
                    </span>
                  </div>
                  <div>
                    <h3 className="text-xl font-metamorphous font-bold text-white leading-none">
                      Secrets
                    </h3>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-slate-900 px-6 py-6 overflow-auto">
              {playerSecrets.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 justify-items-center">
                  {playerSecrets.map((secret) => (
                    <div
                      key={secret.id}
                      className="flex flex-col items-center transform transition-transform hover:-translate-y-1"
                    >
                      <Secret
                        image={secret.image}
                        alt={"Secret"}
                        isRevealed={true}
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  No hay secretos por mostrar.
                </div>
              )}
            </div>

            <div className="bg-slate-950 px-6 py-4 flex flex-col sm:flex-row-reverse items-center gap-3 border-t border-gray-800">
              <button
                onClick={() => setIsModalOpen(false)}
                className="inline-flex items-center justify-center rounded-xl px-6 py-2 text-sm font-metamorphous font-semibold shadow-[0_0_6px_#c2a22d]"
                style={{ background: "#c2a22d", color: "black" }}
                onMouseOver={(e) => {
                  e.currentTarget.style.filter = "brightness(0.95)";
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.filter = "none";
                }}
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
