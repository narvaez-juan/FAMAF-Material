import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import { GameLobby } from "./GameLobby";
import PlayerCard from "../PlayerCard/PlayerCard";

// Mock of player card to isolate tests
vi.mock("../PlayerCard/PlayerCards", () => ({
  default: ({ PlayerName }) => (
    <div data-testid="player-card">{PlayerName}</div>
  ),
}));

describe("GameLobby component", () => {
  const gameMock = {
    id: 1,
    name: "Test Game",
    maxPlayers: 4,
    minPlayers: 2,
    currentPlayers: 2,
    players: [
      { player_id: 101, name: "Alice" },
      { player_id: 102, name: "Bob" },
    ],
  };
  const playersMock = [{ name: "Alice" }, { name: "Bob" }];

  it("renders game name", () => {
    render(
      <GameLobby
        game={gameMock}
        players={playersMock}
        gameReady={false}
        playerId={101}
      />
    );
    expect(screen.getByText("Test Game")).toBeInTheDocument();
  });

  it("renders player count correctly", () => {
    render(
      <GameLobby
        game={gameMock}
        players={playersMock}
        gameReady={false}
        playerId={101}
      />
    );
    expect(
      screen.getByText(
        `Players in lobby: ${playersMock.length} / ${gameMock.maxPlayers}`
      )
    ).toBeInTheDocument();
  });

  it("renders PlayerCard", () => {
    render(
      <GameLobby
        game={gameMock}
        players={playersMock}
        gameReady={false}
        playerId={101}
      />
    );
    const cards = screen.getAllByTestId("player-card");
    expect(cards).toHaveLength(playersMock.length);
    expect(cards[0]).toHaveTextContent("Alice");
    expect(cards[1]).toHaveTextContent("Bob");
  });

  it("shows Start Game button if gameReady is true and player is game creator", () => {
    render(
      <GameLobby
        game={gameMock}
        players={playersMock}
        gameReady={true}
        playerId={101}
      />
    );
    expect(
      screen.getByRole("button", { name: /Start Game/i })
    ).toBeInTheDocument();
  });

  it("shows waiting message if gameReady is true but player is not game creator", () => {
    render(
      <GameLobby
        game={gameMock}
        players={playersMock}
        gameReady={true}
        playerId={102}
      />
    );
    expect(
      screen.getByText(/Waiting for the host to start the game/i)
    ).toBeInTheDocument();
    const button = screen.queryByRole("button", { name: /Start Game/i });
    expect(button).toBeNull();
  });

  it("does not show Start Game button if gameReady is false", () => {
    render(
      <GameLobby
        game={gameMock}
        players={playersMock}
        gameReady={false}
        playerId={101}
      />
    );
    const button = screen.queryByRole("button", { name: /Start Game/i });
    expect(button).toBeNull();
  });
});
