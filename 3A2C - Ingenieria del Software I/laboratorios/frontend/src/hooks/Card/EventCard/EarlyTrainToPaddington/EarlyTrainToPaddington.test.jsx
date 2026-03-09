import { describe, it, vi, expect, beforeEach } from "vitest";
import useEarlyTrainToPaddington from "./EarlyTrainToPaddingtonContainer";
import { createHttpService } from "../../../../services/HTTPServices";
import { emitSelectCard } from "../../../../websocket/emitters/CardEmitter";
import { useEventCardStore } from "../../../../Store/useEventCardStore";

vi.mock("../../../../services/HTTPServices", () => ({
  createHttpService: vi.fn(),
}));

vi.mock("../../../../websocket/emitters/CardEmitter", () => ({
  emitSelectCard: vi.fn(),
}));

vi.mock("../../../../Store/useEventCardStore", () => ({
  useEventCardStore: {
    getState: vi.fn(),
  },
}));

describe("useEarlyTrainToPaddington", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("ejecuta el flujo correctamente", async () => {
    const clearEventCardClicked = vi.fn();
    useEventCardStore.getState.mockReturnValue({ clearEventCardClicked });

    const earlyTrainMock = vi.fn().mockResolvedValue({});
    createHttpService.mockReturnValue({
      earlyTrainToPaddington: earlyTrainMock,
    });

    const card = { id: "card123", name: "24-event_earlytrain.png" };
    const context = { gameId: "gameX", playerId: "playerY" };

    await useEarlyTrainToPaddington(card, context);

    expect(emitSelectCard).toHaveBeenCalledWith(
      "gameX",
      "playerY",
      "Early Train to Paddington",
      "24-event_earlytrain.png",
      null,
      "Event"
    );

    expect(earlyTrainMock).toHaveBeenCalledWith("gameX", "playerY", "card123");
    expect(clearEventCardClicked).toHaveBeenCalled();
  });

  it("no hace nada si card es null", async () => {
    const result = await useEarlyTrainToPaddington(null, {
      gameId: "gameX",
      playerId: "playerY",
    });

    expect(result).toEqual({});
    expect(emitSelectCard).not.toHaveBeenCalled();
  });
});
