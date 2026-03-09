import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import GameCard from "./GameCard";

describe("GameCard", () => {
  const mockOnJoin = vi.fn();

  it("renders game name and player count", () => {
    render(
      <GameCard
        gameName="Mystery Mansion"
        currentPlayers={2}
        maxPlayers={5}
        onJoin={mockOnJoin}
      />
    );

    expect(
      screen.getByRole("heading", { level: 2, name: /Mystery Mansion/i })
    ).toBeInTheDocument();

    expect(screen.getByText(/Players: 2\/5/i)).toBeInTheDocument();
  });

  it("renders join game button", () => {
    render(
      <GameCard
        gameName="Mystery Mansion"
        currentPlayers={2}
        maxPlayers={5}
        onJoin={mockOnJoin}
      />
    );

    expect(
      screen.getByRole("button", { name: /Join Game/i })
    ).toBeInTheDocument();
  });

  it("calls onClick when Join Game button is clicked", () => {
    render(
      <GameCard
        gameName="Mystery Mansion"
        currentPlayers={2}
        maxPlayers={5}
        onJoin={mockOnJoin}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /Join Game/i }));
    expect(mockOnJoin).toHaveBeenCalledTimes(1);
  });
});
