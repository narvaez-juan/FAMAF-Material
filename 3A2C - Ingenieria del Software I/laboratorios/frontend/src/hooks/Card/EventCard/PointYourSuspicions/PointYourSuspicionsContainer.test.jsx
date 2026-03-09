import { describe, it, vi, expect, beforeEach } from "vitest";
import playPointYourSuspicions from "./PointYourSuspicionsContainer";
import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { usePointYourSuspicionsStore } from "../../../../Store/PointYourSuspicionsStore";
import { createHttpService } from "../../../../services/HTTPServices";
import { emitSelectPlayer } from "../../../../websocket/emitters/CardEmitter";

vi.mock("../../../../Store/useEventCardStore", () => {
  const getState = vi.fn();
  return {
    useEventCardStore: Object.assign(vi.fn(), { getState }),
  };
});

vi.mock("../../../../Store/PointYourSuspicionsStore", () => {
  const getState = vi.fn();
  return {
    usePointYourSuspicionsStore: Object.assign(vi.fn(), { getState }),
  };
});

vi.mock("../../../../services/HTTPServices", () => ({
  createHttpService: vi.fn(),
}));

vi.mock("../../../../websocket/emitters/CardEmitter", () => ({
  emitSelectPlayer: vi.fn(),
}));

describe("playPointYourSuspicions", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("ejecuta correctamente todo el flujo del evento Point Your Suspicions", async () => {
    const setPlayerId = vi.fn();
    const setExpectedPlayers = vi.fn();
    const clearSelectedPlayers = vi.fn();
    const waitForAllPlayersSelected = vi
      .fn()
      .mockResolvedValue([
        { target_player_id: "p1" },
        { target_player_id: "p2" },
      ]);

    const clearEventCardClicked = vi.fn();

    usePointYourSuspicionsStore.getState.mockReturnValue({
      setPlayerId,
      setExpectedPlayers,
      clearSelectedPlayers,
      waitForAllPlayersSelected,
    });

    useEventCardStore.getState.mockReturnValue({
      clearEventCardClicked,
    });

    const pointYourSuspicionsMock = vi.fn().mockResolvedValue({});
    createHttpService.mockReturnValue({
      pointYourSuspicions: pointYourSuspicionsMock,
    });

    const card = { id: "card123", name: "Point Your Suspicions" };
    const context = {
      gameId: "gameX",
      playerId: "playerY",
      playersNumber: 2,
    };

    await playPointYourSuspicions(card, context);

    expect(setPlayerId).toHaveBeenCalledWith("playerY");
    expect(setExpectedPlayers).toHaveBeenCalledWith(2);
    expect(emitSelectPlayer).toHaveBeenCalledWith(
      "gameX",
      "playerY",
      "Point Your Suspicions",
      "Point Your Suspicions",
      "Event"
    );

    expect(waitForAllPlayersSelected).toHaveBeenCalledWith(2);

    expect(pointYourSuspicionsMock).toHaveBeenCalledWith(
      "gameX",
      "playerY",
      "card123",
      ["p1", "p2"]
    );

    expect(clearSelectedPlayers).toHaveBeenCalled();
    expect(clearEventCardClicked).toHaveBeenCalled();
  });

  it("retorna vacío si no hay carta", async () => {
    const result = await playPointYourSuspicions(null, {
      gameId: "g",
      playerId: "p",
      playersNumber: 2,
    });
    expect(result).toEqual({});
  });
});
