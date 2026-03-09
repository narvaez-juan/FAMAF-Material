import { describe, it, vi, expect, beforeEach } from "vitest";
import useDeadCardFolly from "./DeadCardFollyContainer";
import { useDeadCardFollyStore } from "../../../../Store/DeadCardFollyStore";
import { createHttpService } from "../../../../services/HTTPServices";
import { emitSelectCard } from "../../../../websocket/emitters/CardEmitter";

vi.mock("../../../../Store/DeadCardFollyStore", () => {
  const getState = vi.fn();
  const setState = vi.fn();
  return {
    useDeadCardFollyStore: Object.assign(vi.fn(), { getState, setState }),
  };
});

vi.mock("../../../../services/HTTPServices", () => ({
  createHttpService: vi.fn(),
}));

vi.mock("../../../../websocket/emitters/CardEmitter", () => ({
  emitSelectCard: vi.fn(),
}));

describe("useDeadCardFolly", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("ejecuta el flujo completo correctamente", async () => {
    const setExpectedPlayers = vi.fn();
    const waitForDirection = vi.fn().mockResolvedValue("left");
    const waitForAllCardsSelected = vi.fn().mockResolvedValue([
      { player_id: "player1", card_id: "cardA" },
      { player_id: "player2", card_id: "cardB" },
    ]);

    useDeadCardFollyStore.getState.mockReturnValue({
      setExpectedPlayers,
      waitForDirection,
      waitForAllCardsSelected,
    });

    const deadCardFollyMock = vi.fn().mockResolvedValue({});
    createHttpService.mockReturnValue({
      deadCardFolly: deadCardFollyMock,
    });

    const card = { id: "event123", name: "Dead Card Folly" };
    const context = { gameId: "gameX", playerId: "playerY", playersNumber: 2 };

    await useDeadCardFolly(card, context);

    expect(useDeadCardFollyStore.setState).toHaveBeenCalledWith({
      selectedCardsByPlayers: [],
    });
    expect(setExpectedPlayers).toHaveBeenCalledWith(2);
    expect(waitForDirection).toHaveBeenCalled();
    expect(emitSelectCard).toHaveBeenCalledWith(
      "gameX",
      "playerY",
      "Dead Card Folly",
      "Dead Card Folly",
      "left",
      "Event"
    );
    expect(waitForAllCardsSelected).toHaveBeenCalledWith(2);
    expect(deadCardFollyMock).toHaveBeenCalledWith(
      "gameX",
      "left",
      [
        ["player1", "cardA"],
        ["player2", "cardB"],
      ],
      "event123"
    );
  });
});
