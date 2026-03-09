import { describe, it, vi, expect, beforeEach } from "vitest";
import playAnotherVictim from "./AnotherVictimContainer";
import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { useAnotherVictimStore } from "../../../../Store/AnotherVictimStore";
import { createHttpService } from "../../../../services/HTTPServices";

vi.mock("../../../../Store/useEventCardStore", () => ({
  useEventCardStore: {
    getState: vi.fn(),
  },
}));

vi.mock("../../../../Store/AnotherVictimStore", () => ({
  useAnotherVictimStore: {
    getState: vi.fn(),
  },
}));

vi.mock("../../../../services/HTTPServices", () => ({
  createHttpService: vi.fn(),
}));

describe("playAnotherVictim", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("llama al flujo correcto (store + http service)", async () => {
    const clearEventCardClicked = vi.fn();

    useEventCardStore.getState.mockReturnValue({
      clearEventCardClicked,
    });

    const setselectPlayerToStealSet = vi.fn();
    const waitForTargetPlayerToStealSet = vi
      .fn()
      .mockResolvedValue({ id: "target123", name: "Bob" });
    const waitForTargetSetToStealId = vi.fn().mockResolvedValue("set456");
    const setNewStolenSet = vi.fn();

    useAnotherVictimStore.getState.mockReturnValue({
      setselectPlayerToStealSet,
      waitForTargetPlayerToStealSet,
      waitForTargetSetToStealId,
      setNewStolenSet,
    });

    const mockStolenSet = {
      id: "set456",
      cards: [{ id: "c1" }, { id: "c2" }],
    };
    const anotherVictim = vi.fn().mockResolvedValue(mockStolenSet);
    createHttpService.mockReturnValue({ anotherVictim });

    const card = { id: "card999", name: "Another Victim" };
    const context = { gameId: "game123", playerId: "player456" };

    await playAnotherVictim(card, context);

    expect(setselectPlayerToStealSet).toHaveBeenCalledWith(true);

    expect(waitForTargetPlayerToStealSet).toHaveBeenCalled();

    expect(waitForTargetSetToStealId).toHaveBeenCalled();

    expect(anotherVictim).toHaveBeenCalledWith(
      "game123",
      "player456",
      "set456",
      "card999"
    );

    expect(setNewStolenSet).toHaveBeenCalledWith(mockStolenSet);

    expect(clearEventCardClicked).toHaveBeenCalled();
  });

  it("maneja correctamente diferentes IDs de jugador y set", async () => {
    const clearEventCardClicked = vi.fn();

    useEventCardStore.getState.mockReturnValue({
      clearEventCardClicked,
    });

    const setselectPlayerToStealSet = vi.fn();
    const waitForTargetPlayerToStealSet = vi
      .fn()
      .mockResolvedValue({ id: "player999", name: "Alice" });
    const waitForTargetSetToStealId = vi.fn().mockResolvedValue("set888");
    const setNewStolenSet = vi.fn();

    useAnotherVictimStore.getState.mockReturnValue({
      setselectPlayerToStealSet,
      waitForTargetPlayerToStealSet,
      waitForTargetSetToStealId,
      setNewStolenSet,
    });

    const mockStolenSet = {
      id: "set888",
      cards: [{ id: "c3" }, { id: "c4" }, { id: "c5" }],
    };
    const anotherVictim = vi.fn().mockResolvedValue(mockStolenSet);
    createHttpService.mockReturnValue({ anotherVictim });

    const card = { id: "card777", name: "Another Victim" };
    const context = { gameId: "game555", playerId: "player333" };

    await playAnotherVictim(card, context);

    expect(anotherVictim).toHaveBeenCalledWith(
      "game555",
      "player333",
      "set888",
      "card777"
    );

    expect(setNewStolenSet).toHaveBeenCalledWith(mockStolenSet);
  });

  it("maneja el flujo completo cuando el set robado está vacío", async () => {
    const clearEventCardClicked = vi.fn();

    useEventCardStore.getState.mockReturnValue({
      clearEventCardClicked,
    });

    const setselectPlayerToStealSet = vi.fn();
    const waitForTargetPlayerToStealSet = vi
      .fn()
      .mockResolvedValue({ id: "target123" });
    const waitForTargetSetToStealId = vi.fn().mockResolvedValue("set456");
    const setNewStolenSet = vi.fn();

    useAnotherVictimStore.getState.mockReturnValue({
      setselectPlayerToStealSet,
      waitForTargetPlayerToStealSet,
      waitForTargetSetToStealId,
      setNewStolenSet,
    });

    const emptyStolenSet = {
      id: "set456",
      cards: [],
    };
    const anotherVictim = vi.fn().mockResolvedValue(emptyStolenSet);
    createHttpService.mockReturnValue({ anotherVictim });

    const card = { id: "card999", name: "Another Victim" };
    const context = { gameId: "game123", playerId: "player456" };

    await playAnotherVictim(card, context);

    expect(setNewStolenSet).toHaveBeenCalledWith(emptyStolenSet);
    expect(clearEventCardClicked).toHaveBeenCalled();
  });
});
