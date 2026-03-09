import { render, screen } from "@testing-library/react";
import { expect, vi } from "vitest";
import GameNotifications from "./GameNotifications";

// Mock de los hooks y useNavigate
vi.mock("../../containers/Game/GameNotificationsContainer", () => ({
  __esModule: true,
  default: vi.fn(),
}));

vi.mock("../../containers/Game/GameInfoContainer", () => ({
  __esModule: true,
  default: vi.fn(),
}));

vi.mock("react-router-dom", () => ({
  useNavigate: vi.fn(),
}));

// Importar después de los mocks
import useGameNotification from "../../containers/Game/GameNotificationsContainer";
import useGameInfo from "../../containers/Game/GameInfoContainer";
import { useNavigate } from "react-router-dom";

function setupMocks({
  actorId = 42,
  targetId = 7,
  reason = "The murderer has been revealed",
  players = [
    { player_id: 42, name: "Hercule Poirot" },
    { player_id: 7, name: "Miss Marple" },
  ],
  notificationType = "game_finished",
  gameInfo,
  gameNotification,
} = {}) {
  const mockNavigate = vi.fn();
  useNavigate.mockReturnValue(mockNavigate);

  useGameNotification.mockReturnValue({
    gameNotification:
      gameNotification !== undefined
        ? gameNotification
        : {
            type: notificationType,
            payload: {
              actor_id: actorId,
              target_id: targetId,
              reason,
              secret_id: 99,
              secret_name: "Eres el asesino",
            },
          },
  });

  useGameInfo.mockReturnValue({
    gameInfo:
      gameInfo !== undefined
        ? gameInfo
        : { players },
  });

  return { mockNavigate };
}

describe("<GameNotifications />", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("debería renderizar correctamente el actor y el motivo", () => {
    setupMocks();
    render(<GameNotifications gameId={123} />);
    expect(screen.getByText(/the murderer has been revealed/i)).toBeInTheDocument();
    expect(
      screen.getByText((text) =>
        text.toLowerCase().includes("revealed by: hercule poirot")
      )
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Exit/i })).toBeInTheDocument();
  });

  it("debería navegar a '/' al hacer clic en el botón Salir", () => {
    const { mockNavigate } = setupMocks();
    render(<GameNotifications gameId={123} />);
    const button = screen.getByRole("button", { name: /Exit/i });
    button.click();
    expect(mockNavigate).toHaveBeenCalledWith("/");
  });

  it("no debería renderizar nada si no hay notificación de juego", () => {
    setupMocks({ gameNotification: null, gameInfo: null });
    const { container } = render(<GameNotifications gameId={123} />);
    expect(container).toBeEmptyDOMElement();
  });

  it("no deberia renderizar el boton si el tipo de evento no es game finished", () => {
    setupMocks({ notificationType: "game_started" });
    render(<GameNotifications gameId={123} />);
    expect(screen.queryByRole("button", { name: /salir/i })).not.toBeInTheDocument();
  });

  it("debería mostrar el actor_id si no hay gameInfo", () => {
    setupMocks({
      gameInfo: null,
      gameNotification: {
        type: "game_finished",
        payload: {
          reason: "The murderer has been revealed",
          actor_id: 42,
          target_id: 7,
          secret_id: 99,
          secret_name: "Eres el asesino",
        },
      },
    });
    render(<GameNotifications gameId={123} />);
    expect(screen.getByText(/revealed by: 42/i)).toBeInTheDocument();
  });

  it("debería mostrar el actor_id si no hay gameInfo.players", () => {
    setupMocks({
      gameInfo: { players: null },
      gameNotification: {
        type: "game_finished",
        payload: {
          reason: "The murderer has been revealed",
          actor_id: 42,
          target_id: 7,
          secret_id: 99,
          secret_name: "Eres el asesino",
        },
      },
    });
    render(<GameNotifications gameId={123} />);
    expect(screen.getByText(/revealed by: 42/i)).toBeInTheDocument();
  });
});