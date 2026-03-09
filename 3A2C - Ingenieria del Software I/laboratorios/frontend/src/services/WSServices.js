const BACKEND_URL =
  import.meta.env.VITE_REACT_APP_WS_URL || "http://localhost:8000";
const DEFAULT_ROOM_ID = "games:list";

let socket;

export default async function getSocket() {
  if (socket) return socket;

  const roomId = localStorage.getItem("RoomID") || DEFAULT_ROOM_ID;
  const { io } = await import("socket.io-client");

  socket = io(BACKEND_URL, {
    path: "/socket.io",
    transports: ["websocket"],
    reconnectionAttempts: 5,
  });

  socket.on("connect", () => {
    console.log("Socket connected", socket.id);
    const roomId = localStorage.getItem("RoomID");
    if (roomId) {
      socket.emit("join_game", roomId);
    }
  });

  return socket;
}

// Esta función asegura que el socket esté conectado antes de devolverlo
export async function getConnectedSocket() {
  const sock = await getSocket();

  if (sock.connected) return sock;

  // Espera hasta que se conecte
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      reject(new Error("Socket connection timeout"));
    }, 5000);

    sock.once("connect", () => {
      clearTimeout(timeout);
      resolve(sock);
    });
  });
}

export async function emit(event, payload) {
  try {
    const sock = await getConnectedSocket();
    sock.emit(event, payload);
  } catch (err) {
    console.error("Failed to emit event:", event, err.message);
  }
}

export async function emitSecrets(gameId, playerId) {
  try {
    const sock = await getConnectedSocket();
    sock.emit("get_secrets", gameId, playerId);
  } catch (err) {
    console.error("Failed to emit secrets event:", err.message);
  }
}
