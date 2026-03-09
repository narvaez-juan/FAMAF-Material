import { render, screen, fireEvent } from "@testing-library/react";
import { vi } from "vitest";
import Decks from "./Decks";

describe("Decks component", () => {
  it("renders draw pile count and discard pile modal", () => {
    render(
      <Decks
        drawPileCount={5}
        drawPilePickCount={2}
        discardPile={["card1", "card2"]}
        setDrawPileLeftClicks={() => {}}
        setDrawPileRightClicks={() => {}}
        totalSelected={0}
        discardedCount={2}
      />
    );

    expect(screen.getByText("5")).toBeInTheDocument();
    expect(screen.getByText("2")).toBeInTheDocument();
    expect(screen.getByText(/Draw Pile/i)).toBeInTheDocument();
  });

  it("calls setDrawPileLeftClicks on left click", () => {
    const leftClickMock = vi.fn();
    render(
      <Decks
        drawPileCount={3}
        drawPilePickCount={0}
        discardPile={[]}
        setDrawPileLeftClicks={leftClickMock}
        setDrawPileRightClicks={() => {}}
        totalSelected={0}
        discardedCount={2}
      />
    );

    const drawPile = screen.getByAltText(/Mazo de cartas/i).closest("div");
    fireEvent.mouseDown(drawPile, { button: 0 });
    expect(leftClickMock).toHaveBeenCalled();
  });

  it("calls setDrawPileRightClicks on right click", () => {
    const rightClickMock = vi.fn();
    render(
      <Decks
        drawPileCount={3}
        drawPilePickCount={0}
        discardPile={[]}
        setDrawPileLeftClicks={() => {}}
        setDrawPileRightClicks={rightClickMock}
        totalSelected={0}
        discardedCount={2}
      />
    );

    const drawPile = screen.getByAltText(/Mazo de cartas/i).closest("div");
    fireEvent.mouseDown(drawPile, { button: 2 });
    expect(rightClickMock).toHaveBeenCalled();
  });
});
