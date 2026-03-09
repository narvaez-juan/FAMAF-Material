import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import StartGame from "./StartGame";

const mockStartGame = vi.fn();

vi.mock("../../services/HTTPServices", () => {
  return {
    createHttpService: () => ({
      startGame: mockStartGame,
    }),
  };
});

describe("StartGame component", () => {
  beforeEach(() => {
    mockStartGame.mockReset();
  });

  it("Calls startGame with game.id and player[0].id on lcick", async () => {
    mockStartGame.mockResolvedValue({ status: 200, data: {} });

    const game = {
      id: "4",
      players: [{ player_id: "1", playerName: "FRANCHESCO" }],
    };

    render(<StartGame game={game} gameReady={true} playerId="1" />);

    const btn = screen.getByRole("button", { name: /start game/i });
    await userEvent.click(btn);

    await waitFor(() => {
      expect(mockStartGame).toHaveBeenCalledTimes(1);
      expect(mockStartGame).toHaveBeenCalledWith("4", "1");
    });
  });

  it("It must show an error when gameStarte returns 406", async () => {
    mockStartGame.mockRejectedValue({ status: 406 });
    const game = {
      id: "4",
      players: [{ player_id: "1", playerName: "FRANCHESCO" }],
    };

    render(<StartGame game={game} gameReady={true} playerId="1" />);

    const btn = screen.getByRole("button", { name: /start game/i });
    await userEvent.click(btn);

    // luego de la promesa rechazada, debe aparecer mensaje de error correspondiente
    await waitFor(() =>
      expect(screen.queryByRole("alert")).toBeInTheDocument()
    );
    expect(screen.getByRole("alert").textContent).toMatch(
      /minimum number of players|not be met|minimo/i
    );
  });

  it("Shows waiting message when player is not the game creator", () => {
    const game = {
      id: "4",
      players: [
        { player_id: "1", playerName: "FRANCHESCO" },
        { player_id: "2", playerName: "ALICE" },
      ],
    };

    render(<StartGame game={game} gameReady={true} playerId="2" />);

    const btn = screen.queryByRole("button", { name: /start game/i });
    expect(btn).toBeNull();

    expect(
      screen.getByText(/Waiting for the host to start the game/i)
    ).toBeInTheDocument();
  });

  it("Does not show anything when gameReady is false", () => {
    const game = {
      id: "4",
      players: [{ player_id: "1", playerName: "FRANCHESCO" }],
    };

    render(<StartGame game={game} gameReady={false} playerId="1" />);

    const btn = screen.queryByRole("button", { name: /start game/i });
    expect(btn).toBeNull();

    const waitingMsg = screen.queryByText(
      /Waiting for the host to start the game/i
    );
    expect(waitingMsg).toBeNull();
  });
});
