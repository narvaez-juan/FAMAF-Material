import { describe, it, vi, expect, beforeEach } from "vitest";
import playDelayMurderEscaped from "./playDelayMurderEscaped";
import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { delayMurderEscapesStore } from "../../../../Store/DelayMurderEscapesStore";
import { createHttpService } from "../../../../services/HTTPServices";

vi.mock("../../../../Store/useEventCardStore", () => {
  const getState = vi.fn();
  return {
    useEventCardStore: Object.assign(vi.fn(), { getState }),
  };
});

vi.mock("../../../../Store/DelayMurderEscapesStore", () => {
  const getState = vi.fn();
  return {
    delayMurderEscapesStore: Object.assign(vi.fn(), { getState }),
  };
});

vi.mock("../../../../services/HTTPServices", () => ({
  createHttpService: vi.fn(),
}));

vi.mock("../../../../websocket/emitters/CardEmitter", () => ({
  emitSelectCard: vi.fn(),
}));

describe("playDelayMurderEscaped", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("ejecuta correctamente todo el flujo del evento Delay Murder Escapes", async () => {
    const setOpenDiscardModal = vi.fn();
    const waitForDiscardCardSelection = vi
      .fn()
      .mockResolvedValue(["card1", "card2"]);
    const clearEventCardClicked = vi.fn();
    const murdererEscapesMock = vi.fn().mockResolvedValue({});

    delayMurderEscapesStore.getState.mockReturnValue({
      setOpenDiscardModal,
      waitForDiscardCardSelection,
    });

    useEventCardStore.getState.mockReturnValue({
      clearEventCardClicked,
    });

    createHttpService.mockReturnValue({
      murdererEscapes: murdererEscapesMock,
    });

    const card = { id: "event777", name: "Delay Murder Escapes" };
    const context = { gameId: "game123", playerId: "player456" };

    await playDelayMurderEscaped(card, context);

    expect(setOpenDiscardModal).toHaveBeenCalledWith(true);
    expect(waitForDiscardCardSelection).toHaveBeenCalled();

    expect(murdererEscapesMock).toHaveBeenCalledWith(
      "game123",
      "player456",
      ["card1", "card2"],
      "event777"
    );

    expect(clearEventCardClicked).toHaveBeenCalled();
  });
});
