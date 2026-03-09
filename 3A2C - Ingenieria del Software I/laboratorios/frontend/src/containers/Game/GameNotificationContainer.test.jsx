import React from "react";
import { render, waitFor, act } from "@testing-library/react";
import { describe, test, expect, vi, beforeEach } from "vitest";

const mockSocket = {
  on: vi.fn(),
  off: vi.fn(),
  connected: true,
};
const mockGetSocket = vi.fn(() => Promise.resolve(mockSocket));
vi.mock("../../services/WSServices", () => ({
  default: (...args) => mockGetSocket(...args),
}));

import useGameNotification from "./GameNotificationsContainer";

function TestComponent({ gameId, onReady }) {
  const state = useGameNotification(gameId);
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

describe("GameNotificationContainer (useGameNotification)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  test("registers notify_winner handler and updates gameNotification when event fires (connected=true)", async () => {
    mockSocket.connected = true;
    const { getState } = await setup("room-1");

    const onCall = mockSocket.on.mock.calls.find(
      (c) => c[0] === "notify_winner"
    );
    expect(onCall).toBeDefined();
    const handler = onCall[1];

    const payload = { winner: "player1", reason: "points" };
    act(() => {
      handler(payload);
    });

    await waitFor(() => {
      const state = getState();
      expect(state.gameNotification).toEqual(payload);
    });
  });

  test("handles socket that connects later (connected=false) and then notifies", async () => {
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

    const notifyCall = mockSocket.on.mock.calls.find(
      (c) => c[0] === "notify_winner"
    );
    expect(notifyCall).toBeDefined();
    const notifyHandler = notifyCall[1];

    const payload = { winner: "player2" };
    act(() => {
      notifyHandler(payload);
    });

    await waitFor(() => {
      const state = getState();
      expect(state.gameNotification).toEqual(payload);
    });
  });

  test("does not throw if getSocket rejects", async () => {
    mockGetSocket.mockRejectedValueOnce(new Error("ws fail"));
    const { getState } = await setup("room-3");

    await waitFor(() => {
      const state = getState();
      expect(state).toBeDefined();
      expect(state.gameNotification).toBeUndefined();
    });
  });
});
