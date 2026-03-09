import React from "react";
import { render, waitFor, act } from "@testing-library/react";
import { describe, test, expect, vi, beforeEach } from "vitest";

/* Mocks before importing the hook */
const mockSocket = {
  on: vi.fn(),
  emit: vi.fn(),
  connected: true,
};
const mockGetSocket = vi.fn(() => Promise.resolve(mockSocket));
vi.mock("../../services/WSServices", () => ({
  default: (...args) => mockGetSocket(...args),
}));

import useGameInfo from "./GameInfoContainer";

function TestComponent({ gameId, onReady }) {
  const state = useGameInfo(gameId);
  React.useEffect(() => {
    onReady(state);
  }, [state]);
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

describe("GameInfoContainer (useGameInfo)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    mockSocket.on.mockClear();
    mockSocket.emit.mockClear();
  });

  test("registers game_info handler and emits get_game_info when connected=true; updates gameInfo when event fires", async () => {
    mockSocket.connected = true;
    const { getState } = await setup("room-1");

    const onCall = mockSocket.on.mock.calls.find((c) => c[0] === "game_info");
    expect(onCall).toBeDefined();
    const handler = onCall[1];

    expect(mockSocket.emit).toHaveBeenCalledWith("get_game_info", "room-1");

    const payload = { players: [{ id: "p1" }], info: "ok" };
    act(() => {
      handler(payload);
    });

    await waitFor(() => {
      const state = getState();
      expect(state.gameInfo).toEqual(payload);
    });
  });

  test("when socket not connected registers connect handler and emits after connect", async () => {
    mockSocket.connected = false;
    const { getState } = await setup("room-2");

    const connectCall = mockSocket.on.mock.calls.find(
      (c) => c[0] === "connect"
    );
    expect(connectCall).toBeDefined();
    const connectHandler = connectCall[1];

    act(() => {
      connectHandler();
    });

    expect(mockSocket.emit).toHaveBeenCalledWith("get_game_info", "room-2");

    const infoCall = mockSocket.on.mock.calls.find((c) => c[0] === "game_info");
    expect(infoCall).toBeDefined();
    const infoHandler = infoCall[1];

    const payload = { players: [], info: "later" };
    act(() => {
      infoHandler(payload);
    });

    await waitFor(() => {
      const state = getState();
      expect(state.gameInfo).toEqual(payload);
    });
  });

  test("does not throw if getSocket rejects", async () => {
    mockGetSocket.mockRejectedValueOnce(new Error("ws fail"));
    const { getState } = await setup("room-3");

    await waitFor(() => {
      const state = getState();
      expect(state).toBeDefined();
      expect(state.gameInfo).toBeUndefined();
    });
  });
});
