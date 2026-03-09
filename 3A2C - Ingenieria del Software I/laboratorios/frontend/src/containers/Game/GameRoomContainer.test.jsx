import React from "react";
import { render, waitFor, act } from "@testing-library/react";
import { describe, test, expect, vi, beforeEach } from "vitest";

const mockFetchPlayerInfo = vi.fn();
vi.mock("../PlayerInfo/PlayerInfoContainer", () => ({
  default: (...args) => mockFetchPlayerInfo(...args),
}));

const mockSocket = {
  on: vi.fn(),
  off: vi.fn(),
  emit: vi.fn(),
  connected: true,
};

const mockGetSocket = vi.fn(() => Promise.resolve(mockSocket));
vi.mock("../../services/WSServices", () => ({
  default: (...args) => mockGetSocket(...args),
}));

import useGameRoomData from "./GameRoomContainer";

function TestComponent({ gameId, onReady }) {
  const state = useGameRoomData(gameId);
  React.useEffect(() => {
    onReady(state);
  }, [state]);
  console.log("STATE", state)
  return null;
}

async function setup(gameId) {
  let state;
  const rendered = render(
    <TestComponent gameId={gameId} onReady={(s) => (state = s)} />
  );
  await waitFor(() => {
    expect(state).toBeDefined();
  });
  return { getState: () => state, ...rendered };
}

describe("GameRoomContainer", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  test("loads initial data, stores RoomID and subscribes to socket, updates on turn_update", async () => {
    mockFetchPlayerInfo.mockResolvedValue({
      jugadores: [{ player_id: "p1" }],
      turnoActual: 5,
      enCurso: true,
    });

    const { getState } = await setup("123");

    await waitFor(() => {
      const state = getState();
      expect(state.loading).toBe(false);
      expect(state.error).toBeNull();
      expect(state.jugadores).toHaveLength(1);
      expect(state.turnoActual).toBe(5);
      expect(state.enCurso).toBe(true);
    });

    expect(localStorage.getItem("RoomID")).toBe("123");

    const onCall = mockSocket.on.mock.calls.find((c) => c[0] === "turn_update");
    expect(onCall).toBeDefined();
    const handler = onCall[1];

    const payload = {
      turnoActual: 7,
      jugadores: [{ player_id: "1" }, { player_id: "2" }],
      enCurso: false,
    };

    act(() => {
      handler(payload);
    });

    await waitFor(() => {
      const state = getState();
      expect(state.turnoActual).toBe(7);
      expect(state.jugadores).toHaveLength(2);
      expect(state.enCurso).toBe(false);
    });
  });

  test("sets error 'Game not found' when fetchPlayerInfo returns 404", async () => {
    mockFetchPlayerInfo.mockRejectedValue({ response: { status: 404 } });
    const { getState } = await setup("room-404");

    await waitFor(() => {
      const state = getState();
      expect(state.loading).toBe(false);
      expect(state.error).toBe("Game not found");
    });
  });

  test("sets WebSocket connection error when getSocket fails", async () => {
    mockFetchPlayerInfo.mockResolvedValue({
      jugadores: [],
      turnoActual: null,
      enCurso: false,
    });
    mockGetSocket.mockRejectedValueOnce(new Error("ws fail"));

    const { getState } = await setup("room-ws-fail");

    await waitFor(() => {
      const state = getState();
      expect(state.loading).toBe(false);
      expect(state.error).toBe("WebSocket connection error");
    });
  });

  test("cleans up socket subscription on unmount", async () => {
    mockFetchPlayerInfo.mockResolvedValue({
      jugadores: [],
      turnoActual: null,
      enCurso: false,
    });

    const { unmount } = render(
      <TestComponent gameId={"room-cleanup"} onReady={() => {}} />
    );

    await waitFor(() => {
      expect(mockSocket.on).toHaveBeenCalled();
    });

    unmount();

    expect(mockSocket.off).toHaveBeenCalledWith("turn_update");
  });
});
