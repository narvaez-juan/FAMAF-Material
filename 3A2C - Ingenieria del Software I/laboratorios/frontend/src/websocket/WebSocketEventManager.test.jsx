import { describe, it, expect, vi, beforeEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import initWebSocketEventManager from "./WebSocketEventManager";
import getSocket from "../services/WSServices";

vi.mock("../services/WSServices", () => ({
  default: vi.fn(),
}));

describe("initWebSocketEventManager", () => {
  let mockSocket;

  beforeEach(() => {
    // Mock completo con off
    mockSocket = {
      on: vi.fn(),
      off: vi.fn(),
      emit: vi.fn(),
      connected: true,
    };

    getSocket.mockResolvedValue(mockSocket);
    vi.clearAllMocks();
  });

  it("llama a getSocket al montar", async () => {
    await act(async () => {
      renderHook(() => initWebSocketEventManager(1));
    });
    expect(getSocket).toHaveBeenCalledOnce();
  });

  it("registra el listener 'card_played_event'", async () => {
    await act(async () => {
      renderHook(() => initWebSocketEventManager(1));
    });
    expect(mockSocket.on).toHaveBeenCalledWith(
      "card_played_event",
      expect.any(Function)
    );
  });

  it("actualiza eventPayload cuando se recibe un evento", async () => {
    let callback;
    mockSocket.on.mockImplementation((event, fn) => {
      if (event === "card_played_event") callback = fn;
    });

    const { result } = renderHook(() => initWebSocketEventManager(1));

    // esperar que monte
    await act(async () => {});

    const payload = { event: "card_played_event", card_name: "Test Card" };

    await act(async () => {
      callback(payload);
    });

    expect(result.current.eventPayload).toEqual(payload);
  });
});
