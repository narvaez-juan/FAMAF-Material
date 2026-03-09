import { describe, test, expect, vi } from "vitest";
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";

import PlayerHandComponent from "./PlayerHandComponent";

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

describe("PlayerHandComponent (Presentational)", () => {
  const defaultProps = {
    loading: false,
    playerHand: [
      { gameCardId: 1, image: "img1.png" },
      { gameCardId: 2, image: "img2.png" },
    ],
    selectedCards: [],
    isDiscardDisabled: true,
    isFinishDisabled: false,
    finishLoading: false,
    finishError: null,
    onDiscardCard: vi.fn(),
    onFinishClick: vi.fn(),
    onCardClick: vi.fn(),
  };

  test("should render loading state correctly", () => {
    render(<PlayerHandComponent {...defaultProps} loading={true} />);
    expect(screen.getByText("End Turn(60)")).toBeInTheDocument();
  });

  test("should render player cards when not loading", () => {
    render(<PlayerHandComponent {...defaultProps} />);
    expect(screen.getByText("Card 2")).toBeInTheDocument();
    const cards = screen.getAllByTestId("card");
    expect(cards).toHaveLength(2);
    expect(cards[0]).toHaveAttribute("aria-label", "Card 1");
  });

  test("should render 'no cards' message when hand is empty", () => {
    render(<PlayerHandComponent {...defaultProps} playerHand={[]} />);
    expect(
      screen.getByText("You don't have cards in your hand.")
    ).toBeInTheDocument();
  });

  test("should call onCardClick when a card is clicked", () => {
    render(<PlayerHandComponent {...defaultProps} />);
    const cards = screen.getAllByTestId("card");
    fireEvent.click(cards[0]);
    expect(defaultProps.onCardClick).toHaveBeenCalledWith(1, "img1.png");
  });

  test("should call onDiscardCard when discard button is clicked", () => {
    render(<PlayerHandComponent {...defaultProps} isDiscardDisabled={false} />);
    const discardButton = screen.getByText(/Discard/);
    fireEvent.click(discardButton);
    expect(defaultProps.onDiscardCard).toHaveBeenCalled();
  });

  test("should call onFinishClick when finish turn button is clicked", () => {
    render(<PlayerHandComponent {...defaultProps} />);
    const finishButton = screen.getByText("End Turn(60)");
    fireEvent.click(finishButton);
    expect(defaultProps.onFinishClick).toHaveBeenCalled();
  });

  test("buttons should be disabled ", () => {
    render(
      <PlayerHandComponent
        {...defaultProps}
        isDiscardDisabled={true}
        isFinishDisabled={true}
      />
    );
    expect(screen.getByText(/Discard/)).toBeDisabled();
    expect(screen.getByText("End Turn(60)")).toBeDisabled();
  });

  test("should display finish error message", () => {
    const errorMessage = "Hubo un error";
    render(
      <PlayerHandComponent {...defaultProps} finishError={errorMessage} />
    );
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });
});
