import { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import Secret from "../Secret/Secret"; // Asume que tienes este componente
import getSocket from "../../services/WSServices";

export default function OponentSecrets({ jugador, playerId }) {
  const { gameId } = useParams();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [oponentSecrets, setOponentSecrets] = useState([]);
  const socketRef = useRef(null);
  const [loading, setLoading] = useState(true);

  const handleSecretPayload = (payload) => {
    try {
      if (payload.player_id === jugador.id_jugador) {
        setOponentSecrets(payload.secrets_list);
      }
    } catch (error) {
      console.error("Error manejando payload de secretos del oponente:", error);
    }
  };

  useEffect(() => {
    let mounted = true;

    const connect = async () => {
      try {
        if (!localStorage.getItem("RoomID") && gameId) {
          localStorage.setItem("RoomID", gameId);
        }

        const sock = await getSocket();
        socketRef.current = sock;

        // pedir los secretos del jugador
        // inmediatamente luego de getSocket() porque
        // esto maneja la conexión
        sock.emit("get_secrets", gameId, jugador.id_jugador);

        const onConnect = () => {
          // pedir secretos al conectarse
          sock.emit("get_secrets", gameId, jugador.id_jugador);
        };

        // Registrar listeners
        sock.on("connect", onConnect);
        sock.on("player_secrets", handleSecretPayload);

        if (mounted) setLoading(false);
      } catch (err) {
        console.error("Socket connection failed:", err);
        if (mounted) setLoading(false);
      }
    };

    connect();

    return () => {};
  }, [gameId, jugador.id_jugador]);

  return (
    <>
      {/* Botón para ver secretos del oponente */}
      <button
        onClick={() => setIsModalOpen(true)}
        className="w-full mt-2 px-3 py-1.5 rounded-lg text-sm font-metamorphous font-semibold transition-all duration-200 border border-yellow-600/50 hover:border-yellow-400 shadow-[0_0_4px_rgba(194,162,45,0.3)] hover:shadow-[0_0_8px_rgba(194,162,45,0.6)]"
        style={{ background: "#0b3b6f", color: "white" }}
        onMouseOver={(e) => {
          e.currentTarget.style.background = "#c2a22d";
          e.currentTarget.style.color = "black";
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.background = "#0b3b6f";
          e.currentTarget.style.color = "white";
        }}
      >
        See Secrets
      </button>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div
            className="absolute inset-0 bg-black/80 backdrop-blur-sm"
            onClick={() => setIsModalOpen(false)}
          />
          <div className="relative w-full max-w-4xl max-h-[84vh] overflow-hidden rounded-2xl shadow-2xl border border-gray-700 z-50">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-900 to-black px-6 py-5 border-b border-yellow-400">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-md bg-gradient-to-br from-[#112b57] to-[#0b3b6f] flex items-center justify-center shadow-[0_0_4px_#c2a22d]">
                    <span className="text-3xl font-metamorphous font-bold text-[#c2a22d]">
                      {jugador.nombre.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-xl font-metamorphous font-bold text-white leading-none">
                      Secrets of {jugador.nombre}
                    </h3>
                    <p className="text-sm text-gray-400 mt-1">
                      {oponentSecrets.length || 0} secretos
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Content */}
            <div className="bg-slate-900 px-6 py-6 overflow-auto max-h-[calc(84vh-180px)]">
              {oponentSecrets && oponentSecrets.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 justify-items-center">
                  {oponentSecrets.map((secret, index) => (
                    <div
                      key={secret.id || index}
                      className="flex flex-col items-center"
                    >
                      <Secret
                        image={secret.image}
                        alt={`Secret ${index + 1}`}
                        isRevealed={
                          jugador.id_jugador === playerId
                            ? true
                            : secret.isRevealed
                        }
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <p className="text-gray-400 font-metamorphous">
                    This player dont have secrets
                  </p>
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="bg-slate-950 px-6 py-4 flex flex-col sm:flex-row-reverse items-center gap-3 border-t border-gray-800">
              <button
                onClick={() => setIsModalOpen(false)}
                className="inline-flex items-center justify-center rounded-xl px-6 py-2 text-sm font-metamorphous font-semibold shadow-[0_0_6px_#c2a22d] transition-all"
                style={{ background: "#c2a22d", color: "black" }}
                onMouseOver={(e) => {
                  e.currentTarget.style.filter = "brightness(0.95)";
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.filter = "none";
                }}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
