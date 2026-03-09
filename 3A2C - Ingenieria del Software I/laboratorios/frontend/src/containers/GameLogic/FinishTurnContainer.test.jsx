import React from "react";
import { render, waitFor, act } from "@testing-library/react";
import { describe, test, expect, vi, beforeEach } from "vitest";
import useFinishTurn from "./FinishTurnContainer";

//NOTE - Mock HTTP service used by the hook
const mockHttpService = {
  discardCard: vi.fn(),
  drawCard: vi.fn(),
  finishTurn: vi.fn(),
};

vi.mock("../../services/HTTPServices", () => ({
  createHttpService: vi.fn(() => mockHttpService),
}));

function TestComponent({ onReady }) {
  const htppservice = useFinishTurn();
  React.useEffect(() => {
    onReady(htppservice);
  }, []);
  return null;
}

//NOTE - Fixture to initialize the hook
async function setup() {
  let htppservice;
  render(<TestComponent onReady={(a) => (htppservice = a)} />);
  await waitFor(() => {
    expect(htppservice).toBeDefined();
  });
  return htppservice;
}

describe("FinishTurnContainer", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("when playerHasDiscarded=false it discards a card, draws, finishes and draws additional cards", async () => {
    mockHttpService.discardCard.mockResolvedValue({});
    mockHttpService.drawCard.mockResolvedValue({});
    mockHttpService.finishTurn.mockResolvedValue({});

    const httpService = await setup();

    const gameId = "111";
    const playerId = "1";
    const playerHand = [
      { gameCardId: 100, card_id: 1 },
      { gameCardId: 136, card_id: 9 },
    ];

    await act(async () => {
      await httpService.finish(gameId, playerId, false, false, playerHand, 2);
    });

    expect(mockHttpService.discardCard).toHaveBeenCalledWith(gameId, playerId, [
      136,
    ]);
    expect(mockHttpService.drawCard).toHaveBeenCalledTimes(2);
    expect(mockHttpService.drawCard).toHaveBeenCalledWith(
      gameId,
      playerId,
      [],
      1
    );
    expect(mockHttpService.finishTurn).toHaveBeenCalledWith(gameId, playerId);
    expect(mockHttpService.drawCard).toHaveBeenCalledWith(
      gameId,
      playerId,
      [],
      2
    );
  });

  test("when playerHasDiscarded=true it skips discard but draws additional cards after finish", async () => {
    mockHttpService.discardCard.mockResolvedValue({});
    mockHttpService.drawCard.mockResolvedValue({});
    mockHttpService.finishTurn.mockResolvedValue({});

    const httpService = await setup();

    const gameId = "2";
    const playerId = "2";

    await act(async () => {
      await httpService.finish(gameId, playerId, true, false, [], 3);
    });

    expect(mockHttpService.discardCard).not.toHaveBeenCalled();
    expect(mockHttpService.finishTurn).toHaveBeenCalledWith(gameId, playerId);
    expect(mockHttpService.drawCard).toHaveBeenCalledWith(
      gameId,
      playerId,
      [],
      3
    );
  });

  test("propagates errors from underlying HTTP calls", async () => {
    const error = new Error("boom");
    mockHttpService.discardCard.mockRejectedValue(error);

    const httpService = await setup();

    await expect(
      act(async () => {
        await httpService.finish(
          "g",
          "p",
          false,
          false,
          [{}, { gameCardId: 1 }],
          0
        );
      })
    ).rejects.toBeDefined();
  });
});
