import { describe, test, expect, vi } from "vitest";
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import DraftPileComponent from "./DraftPileComponent";

vi.mock("../Card/Card", () => ({
  default: ({ alt, onClick, isSelected }) => (
    <div
      data-testid="card"
      onClick={onClick}
      className={isSelected ? "selected" : ""}
      aria-label={alt}
    >
      {alt}
    </div>
  ),
}));

describe("DraftPileComponent", () => {
  const defaultProps = {
    loading: false,
    draftPile: [
      { gameCardId: 1, image: "AAAAAAAAAAAAAAAAAAAAAAAAa.png" },
      { gameCardId: 2, image: "BBBBBBBBBBBBBBBBBBBBBBBBb.png" },
    ],
    selectedCards: [],
    handleCardClick: vi.fn(),
  };

  test("should render 'no cards' message when draft pile is empty", () => {
    render(<DraftPileComponent {...defaultProps} draftPile={[]} />);
    expect(screen.getByText("No cards in draft pile.")).toBeInTheDocument();
  });

  test("Should call handleCardClick when a card is clicked", () => {
    render(<DraftPileComponent {...defaultProps} />);
    const cards = screen.getAllByTestId("card");
    fireEvent.click(cards[0]);
    expect(defaultProps.handleCardClick).toHaveBeenCalledWith(1);
  });

  test("Should show selected class when card is selected", () => {
    render(<DraftPileComponent {...defaultProps} selectedCards={[1]} />);
    const cards = screen.getAllByTestId("card");
    expect(cards[0]).toHaveClass("selected");
    expect(cards[1]).not.toHaveClass("selected");
  });
});
