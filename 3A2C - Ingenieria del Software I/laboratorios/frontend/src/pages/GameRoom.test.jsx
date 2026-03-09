import React from "react";
import { render, screen, waitFor, act } from "@testing-library/react";
import { describe, test, expect, vi, beforeEach } from "vitest";

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useParams: () => ({ gameId: "room-xyz" }),
    useLocation: () => ({ state: { playerId: "player-42" } }),
  };
});

const mockUseGameRoomData = vi.fn();
vi.mock("../containers/Game/GameRoomContainer", () => ({
  __esModule: true,
  default: (gameId) => mockUseGameRoomData(gameId),
}));

vi.mock("../containers/Deck/DiscardPileContainer", () => ({
  __esModule: true,
  default: vi.fn(() => ({ discardPile: ["d1"] })),
}));
vi.mock("../containers/Deck/DrawPileContainer", () => ({
  __esModule: true,
  default: vi.fn(() => ({ drawPile: ["r1"] })),
}));

vi.mock("../components/StatusMessage/StatusMessage", () => ({
  __esModule: true,
  default: ({ message }) => <div data-testid="status-message">{message}</div>,
}));

vi.mock("../components/GameNotifications/GameNotifications", () => ({
  __esModule: true,
  default: () => <div data-testid="game-notifications" />,
}));

vi.mock("../containers/PlayerHand/PlayerHandContainer", () => ({
  __esModule: true,
  default: () => <div data-testid="player-hand-mock" />,
}));

vi.mock("../components/GameTable/GameTable", () => ({
  __esModule: true,
  default: (props) => (
    <div
      data-testid="game-table"
      data-jugadores={JSON.stringify(props.jugadores)}
      data-turno={String(props.turnoActual)}
      data-discard={JSON.stringify(props.discardPile)}
      data-draw={JSON.stringify(props.drawPile)}
      data-playerid={props.playerId}
      data-gameid={props.gameId}
    />
  ),
  GameTable: (props) => (
    <div
      data-testid="game-table"
      data-jugadores={JSON.stringify(props.jugadores)}
      data-turno={String(props.turnoActual)}
      data-discard={JSON.stringify(props.discardPile)}
      data-draw={JSON.stringify(props.drawPile)}
      data-playerid={props.playerId}
      data-gameid={props.gameId}
    />
  ),
}));

import GameRoom from "./GameRoom";

describe("GameRoom page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  test("shows loading status when loading is true", async () => {
    mockUseGameRoomData.mockReturnValue({
      jugadores: [],
      turnoActual: null,
      loading: true,
      error: null,
      enCurso: false,
    });

    render(<GameRoom />);

    expect(await screen.findByTestId("status-message")).toHaveTextContent(
      "Loading game..."
    );
  });

  test("shows error status when error is set", async () => {
    mockUseGameRoomData.mockReturnValue({
      jugadores: [],
      turnoActual: null,
      loading: false,
      error: "Some error happened",
      enCurso: false,
    });

    render(<GameRoom />);

    expect(await screen.findByTestId("status-message")).toHaveTextContent(
      "Some error happened"
    );
  });

  test("shows not-started message when enCurso is false", async () => {
    mockUseGameRoomData.mockReturnValue({
      jugadores: [],
      turnoActual: null,
      loading: false,
      error: null,
      enCurso: false,
    });

    render(<GameRoom />);

    expect(await screen.findByTestId("status-message")).toHaveTextContent(
      "The game has not started yet"
    );
  });

  test("renders GameTable when enCurso is true and passes piles + ids", async () => {
    const jugadores = [{ player_id: "player-42", name: "Test" }];
    mockUseGameRoomData.mockReturnValue({
      jugadores,
      turnoActual: 3,
      loading: false,
      error: null,
      enCurso: true,
    });

    render(<GameRoom />);

    await waitFor(() => {
      expect(screen.queryByTestId("status-message")).toBeNull();
    });

    const table = await screen.findByTestId("game-table");
    expect(table).toBeDefined();
    expect(table.getAttribute("data-turno")).toBe("3");
    expect(table.getAttribute("data-playerid")).toBe("player-42");
    expect(table.getAttribute("data-gameid")).toBe("room-xyz");
    expect(table.getAttribute("data-discard")).toBe(JSON.stringify(["d1"]));
    expect(table.getAttribute("data-draw")).toBe(JSON.stringify(["r1"]));
  });
});
