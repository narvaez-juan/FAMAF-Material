import { describe, it, vi, expect, beforeEach } from "vitest";
import playLookIntoTheAshes from "./LookIntoTheAshesContainer";
import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { intoTheAshesStore } from "../../../../Store/IntoTheAshesStore";
import { createHttpService } from "../../../../services/HTTPServices";

vi.mock("../../../../Store/useEventCardStore", () => {
  const getState = vi.fn();
  return {
    useEventCardStore: Object.assign(vi.fn(), { getState }),
  };
});

vi.mock("../../../../Store/IntoTheAshesStore", () => {
  const getState = vi.fn();
  return {
    intoTheAshesStore: Object.assign(vi.fn(), { getState }),
  };
});

vi.mock("../../../../services/HTTPServices", () => ({
  createHttpService: vi.fn(),
}));

vi.mock("../../../../websocket/emitters/CardEmitter", () => ({
  emitSelectCard: vi.fn(),
}));

describe("playLookIntoTheAshes", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("ejecuta correctamente todo el flujo del evento Look Into The Ashes", async () => {
    const setOpenModal = vi.fn();
    const waitForSelectedCardToDraw = vi.fn().mockResolvedValue("card123");
    const clearEventCardClicked = vi.fn();
    const lookIntoTheAshesMock = vi.fn().mockResolvedValue({});

    intoTheAshesStore.getState.mockReturnValue({
      setOpenModal,
      waitForSelectedCardToDraw,
    });

    useEventCardStore.getState.mockReturnValue({
      clearEventCardClicked,
    });

    createHttpService.mockReturnValue({
      lookIntoTheAshes: lookIntoTheAshesMock,
    });

    const card = { id: "event999", name: "Look Into The Ashes" };
    const context = { gameId: "gameABC", playerId: "playerXYZ" };

    await playLookIntoTheAshes(card, context);

    expect(setOpenModal).toHaveBeenCalledWith(true);
    expect(waitForSelectedCardToDraw).toHaveBeenCalled();

    expect(lookIntoTheAshesMock).toHaveBeenCalledWith(
      "gameABC",
      "playerXYZ",
      "event999",
      "card123"
    );

    expect(clearEventCardClicked).toHaveBeenCalled();
  });
});
