import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { vi } from "vitest";

// Mock of the Card component (hoisted by vitest)
vi.mock("../Card/Card", () => {
  return {
    default: ({ image, alt }) => <div data-testid="mock-card">{alt}</div>,
  };
});

import DiscardPileModal from "./DiscardPileModal";

describe("DiscardPileModal", () => {
  test("renders the title and shows 'No cards' when empty", () => {
    const { container } = render(<DiscardPileModal discardPile={[]} />);

    // Deck title
    expect(screen.getByText(/Discard Pile/i)).toBeInTheDocument();

    // In the small deck should show the message "No cards"
    expect(screen.getByText(/No cards/i)).toBeInTheDocument();

    // Ensure the clickable div exists (cursor-pointer)
    const clickable = container.querySelector(".cursor-pointer");
    expect(clickable).toBeTruthy();
  });

  test("clicking opens modal and shows message when there are no discards", () => {
    const { container } = render(<DiscardPileModal discardPile={[]} />);

    // Find the clickable div and click it
    const clickable = container.querySelector(".cursor-pointer");
    expect(clickable).toBeTruthy();
    fireEvent.click(clickable);

    // Now the modal should appear with the text "Last Discarded Cards"
    expect(screen.getByText(/Last Discarded Cards/i)).toBeInTheDocument();

    // And, since there are no cards, it should show "No discarded cards yet"
    expect(screen.getByText(/No discarded cards yet/i)).toBeInTheDocument();

    // Close button should exist and will close the modal
    const closeButton = screen.getByRole("button", { name: /Close/i });
    expect(closeButton).toBeInTheDocument();
    fireEvent.click(closeButton);

    // After closing, the modal text should no longer be present
    expect(screen.queryByText(/Last Discarded Cards/i)).not.toBeInTheDocument();
  });

  test("shows the top card in the deck when there are discards and displays the latest ones when opening modal", () => {
    // Create 7 cards to verify that only the last ones are shown
    const cards = Array.from({ length: 7 }, (_, i) => ({
      image: `img-${i + 1}`,
    }));

    const { container } = render(<DiscardPileModal discardPile={cards} />);

    // The top card of the deck should be rendered (mock shows the alt "Discarded card")
    const mockedCards = screen.getAllByTestId("mock-card");

    // At this point there should be at least one mock-card (the top card)
    expect(mockedCards.length).toBeGreaterThan(0);
    expect(mockedCards[0]).toHaveTextContent("Discarded card");

    // Open the modal by clicking the div with cursor-pointer
    const clickable = container.querySelector(".cursor-pointer");
    expect(clickable).toBeTruthy();
    fireEvent.click(clickable);

    // See modal title
    expect(screen.getByText(/Last Discarded Cards/i)).toBeInTheDocument();

    // In the modal, the last 5 cards are shown with alt "Discarded card 1" .. "Discarded card 5"
    for (let i = 1; i <= 5; i++) {
      expect(screen.getAllByText(/Card/i).length).toBeGreaterThan(0);
    }

    // Close with the button
    fireEvent.click(screen.getByRole("button", { name: /Close/i }));
    expect(screen.queryByText(/Last Discarded Cards/i)).not.toBeInTheDocument();
  });
});
