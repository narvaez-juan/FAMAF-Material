import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { describe, test, expect, vi, beforeEach, afterEach } from "vitest";
import Lobby from "./Lobby";
import { MemoryRouter } from "react-router-dom";

const mockNavigate = vi.fn();

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
    useParams: () => ({ gameId: "1" }),
    useLocation: () => ({ state: { playerId: "FRan" } }),
  };
});

//NOTE Mock of socket module
vi.mock("../services/WSServices", () => ({
  default: vi.fn(),
}));

import getSocket from "../services/WSServices";

describe("Lobby integration with sockets", () => {
  let mockSocket;

  beforeEach(() => {
    //NOTE Clear mocks and localstorage
    vi.clearAllMocks();
    localStorage.clear();

    mockSocket = {
      id: "socket-1",
      emit: vi.fn(),
      on: vi.fn(),
      off: vi.fn(),
    };

    getSocket.mockResolvedValue(mockSocket);
  });

  afterEach(() => {
    //NOTE Delete all data added to localstorage
    localStorage.clear();
  });

  //SECTION - sets RoomID and emits join_game and get_game_info
  test("on mount: sets RoomID and emits join_game and get_game_info", async () => {
    render(
      <MemoryRouter initialEntries={["/games/1/lobbies"]}>
        <Lobby />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(getSocket).toHaveBeenCalled();
    });

    await waitFor(() => {
      expect(mockSocket.emit).toHaveBeenCalledWith("join_game", "1");
      expect(mockSocket.emit).toHaveBeenCalledWith("get_game_info", "1");
    });

    //NOTE Expect RoomId to be save on localstorage
    expect(localStorage.getItem("RoomID")).toBe("1");
  });
  //!SECTION
  //SECTION - Process game_info and update players (renders game name and player list
  test("Process game_info and update players (renders game name and player list)", async () => {
    render(
      <MemoryRouter initialEntries={["/games/1/lobbies"]}>
        <Lobby />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(mockSocket.on).toHaveBeenCalled();
      expect(mockSocket.on).toHaveBeenCalledWith(
        "game_info",
        expect.any(Function)
      );
    });

    const gameInfoCall = mockSocket.on.mock.calls.find(
      ([evt]) => evt === "game_info"
    );
    expect(gameInfoCall).toBeTruthy();

    const gameInfoHandler = gameInfoCall[1];

    const gameInfo = {
      id: "1",
      name: "newGame",
      players: [{ name: "Fetucini" }],
      currentPlayers: 1,
      minPlayers: 1,
      maxPlayers: 4,
    };

    gameInfoHandler(gameInfo);

    await waitFor(() => {
      expect(screen.getByText(/newGame/)).toBeInTheDocument();

      const playersHeading = screen.getByText(/Players in lobby:/);
      expect(playersHeading).toBeInTheDocument();
      expect(playersHeading.textContent.replace(/\s+/g, " ")).toMatch(
        /Players in lobby: 1 \/ 4/
      );

      const cards = screen.queryAllByTestId("player-card");
      expect(cards.length).toBe(1);

      expect(screen.getByText(/Fetucini/)).toBeInTheDocument();
    });
  });
  //!SECTION
  //SECTION - Handle new player on player_joined (appends player to list)
  test("Handle new player on player_joined (appends player to list)", async () => {
    render(
      <MemoryRouter initialEntries={["/games/1/lobbies"]}>
        <Lobby />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(mockSocket.on).toHaveBeenCalledWith(
        "player_joined",
        expect.any(Function)
      );
    });

    const playerJoinedCall = mockSocket.on.mock.calls.find(
      ([evt]) => evt === "player_joined"
    );
    expect(playerJoinedCall).toBeTruthy();
    const playerJoinedHandler = playerJoinedCall[1];

    playerJoinedHandler({ playerName: "Fideos con Salsa" });

    //NOTE - New Player expected to be on the UI
    await waitFor(() => {
      expect(screen.getByText(/Fideos con Salsa/)).toBeInTheDocument();
      const cards = screen.queryAllByTestId("player-card");
      expect(cards.length).toBeGreaterThanOrEqual(1);
    });
  });
  //!SECTION
  //SECTION - Handle game_started: navigates to game route with playerId state
  test("Handle game_started: navigates to game route with playerId state", async () => {
    render(
      <MemoryRouter initialEntries={["/games/1/lobbies"]}>
        <Lobby />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(mockSocket.on).toHaveBeenCalledWith(
        "game_started",
        expect.any(Function)
      );
    });

    const gameStartedCall = mockSocket.on.mock.calls.find(
      ([evt]) => evt === "game_started"
    );
    expect(gameStartedCall).toBeTruthy();
    const gameStartedHandler = gameStartedCall[1];

    const payload = { id: "42" };
    gameStartedHandler(payload);

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith(`/games/42`, {
        state: { playerId: "FRan" },
      });
    });
  });
  //!SECTION
  //SECTION - Handle initial_hand: stores initial hand in localStorage
  test("Handle initial_hand: stores initial hand in localStorage", async () => {
    render(
      <MemoryRouter initialEntries={["/games/1/lobbies"]}>
        <Lobby />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(mockSocket.on).toHaveBeenCalledWith(
        "initial_hand",
        expect.any(Function)
      );
    });

    const initialHandCall = mockSocket.on.mock.calls.find(
      ([evt]) => evt === "initial_hand"
    );
    expect(initialHandCall).toBeTruthy();
    const initialHandHandler = initialHandCall[1];

    const handPayload = { player_id: "FRan", cards: [7, 8, 9] };

    initialHandHandler(handPayload);

    await waitFor(() => {
      const stored = localStorage.getItem("initialHand");
      expect(stored).toBeTruthy();
      expect(JSON.parse(stored)).toEqual(handPayload);
    });
  });
});
//!SECTION
