import { describe, it, expect, vi, beforeEach } from "vitest";
import { renderHook, act, waitFor } from "@testing-library/react";
import useSets from "./PlaySetContainer";

// Mock del servicio de WebSocket
vi.mock("../../services/WSServices", () => ({
  default: vi.fn(),
}));

import getSocket from "../../services/WSServices";

describe("useSets (PlaySetContainer)", () => {
  let mockSocket;

  beforeEach(() => {
    vi.clearAllMocks();

    mockSocket = {
      on: vi.fn(),
      off: vi.fn(),
      emit: vi.fn(),
    };

    getSocket.mockResolvedValue(mockSocket);
  });

  it("registra listeners correctamente", async () => {
    renderHook(() => useSets(55, 10));

    await waitFor(() => {
      expect(mockSocket.on).toHaveBeenCalledWith(
        "player_sets_updated",
        expect.any(Function)
      );
      expect(mockSocket.on).toHaveBeenCalledWith(
        "target_chooses_secret",
        expect.any(Function)
      );
      expect(mockSocket.on).toHaveBeenCalledWith(
        "emit_player_sets",
        expect.any(Function)
      );
    });
  });

  it("emite get_player_sets cuando se llama fetchPlayerSets", async () => {
    const { result } = renderHook(() => useSets(55, 10));

    await waitFor(() => expect(getSocket).toHaveBeenCalled());

    act(() => {
      result.current.fetchPlayerSets(99);
    });

    expect(mockSocket.emit).toHaveBeenCalledWith("get_player_sets", {
      game_id: 55,
      player_id: 99,
    });
  });

  it("actualiza requestedPlayerSets cuando llega emit_player_sets", async () => {
    const { result } = renderHook(() => useSets(55, 10));

    await waitFor(() =>
      expect(mockSocket.on).toHaveBeenCalledWith(
        "emit_player_sets",
        expect.any(Function)
      )
    );

    const handler = mockSocket.on.mock.calls.find(
      ([event]) => event === "emit_player_sets"
    )?.[1];

    const payload = {
      sets: [{ set_play_id: 1, card_game_ids: [1, 2], visible_to_all: true }],
    };

    act(() => {
      handler(payload);
    });

    expect(result.current.requestedPlayerSets).toEqual(payload.sets);
    expect(result.current.isLoadingSets).toBe(false);
  });

  it("actualiza allSets cuando llega player_sets_updated", async () => {
    const { result } = renderHook(() => useSets(55, 10));

    await waitFor(() =>
      expect(mockSocket.on).toHaveBeenCalledWith(
        "player_sets_updated",
        expect.any(Function)
      )
    );

    const handler = mockSocket.on.mock.calls.find(
      ([event]) => event === "player_sets_updated"
    )?.[1];

    const payload = {
      players_sets: [
        {
          player_id: 10,
          sets: [
            { set_play_id: 1, card_game_ids: [1, 2], visible_to_all: true },
          ],
        },
      ],
    };

    act(() => {
      handler(payload);
    });

    expect(result.current.allSets).toEqual(payload.players_sets);
  });
});
