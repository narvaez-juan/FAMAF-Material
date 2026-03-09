import React from "react";
import { render, waitFor, act } from "@testing-library/react";
import { describe, test, expect, vi, beforeEach } from "vitest";
import useDrawCard from "./DrawCardContainer";

const mockHttpService = {
  drawCard: vi.fn(),
};

vi.mock("../../services/HTTPServices", () => ({
  createHttpService: vi.fn(() => mockHttpService),
}));

function TestComponent({ onReady }) {
  const drawCard = useDrawCard();
  React.useEffect(() => {
    onReady(drawCard);
  }, []);
  return null;
}

//NOTE - Fixture to initialize the hook
async function setup() {
  let drawCardFn;
  render(<TestComponent onReady={(fn) => (drawCardFn = fn)} />);
  await waitFor(() => {
    expect(drawCardFn).toBeDefined();
  });
  return drawCardFn;
}

describe("DrawCardContainer", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("calls drawCard with the right parameters", async () => {
    mockHttpService.drawCard.mockResolvedValue({ success: true });

    const drawCard = await setup();

    const gameId = "1";
    const playerId = "1";
    const selectedDraftCards = [1, 2];
    const selectedDrawCardsNumber = 3;

    await act(async () => {
      await drawCard(
        gameId,
        playerId,
        selectedDraftCards,
        selectedDrawCardsNumber
      );
    });

    expect(mockHttpService.drawCard).toHaveBeenCalledWith(
      gameId,
      playerId,
      selectedDraftCards,
      selectedDrawCardsNumber
    );
  });

  test("propaga errores del servicio HTTP", async () => {
    const error = new Error("fail");
    mockHttpService.drawCard.mockRejectedValue(error);

    const drawCard = await setup();

    await expect(
      act(async () => {
        await drawCard("1", "1", [], 1);
      })
    ).rejects.toBeDefined();
  });
});
