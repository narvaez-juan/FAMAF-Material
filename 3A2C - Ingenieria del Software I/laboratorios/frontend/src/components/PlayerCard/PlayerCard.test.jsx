import { describe, it, expect } from "vitest";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import PlayerCard from "./PlayerCard";

describe("PlayerCard component", () => {
  it("renders player name correctly", () => {
    render(<PlayerCard PlayerName="Pedro" />);
    
    const playerNameElement = screen.getByText("Pedro");
    expect(playerNameElement).toBeInTheDocument();
    expect(playerNameElement).toHaveClass("tracking-wide");
    expect(playerNameElement).toHaveClass("text-2xl");
  });

  it("truncates long names correctly", () => {
    const longName = "ThisIsAnExcessivelyLongPlayerNameThatShouldBeTruncated";
    render(<PlayerCard PlayerName={longName} />);
    
    const playerNameElement = screen.getByText(longName);
    expect(playerNameElement).toBeInTheDocument();
    expect(playerNameElement).toHaveClass("truncate");
  });
});
