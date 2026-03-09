import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import GameTable from "./GameTable";

vi.mock("../PlayerInfo/PlayerInfo", () => ({ default: vi.fn(() => null) }));
vi.mock("../Decks/Decks", () => ({ default: vi.fn(() => null) }));
vi.mock("../PlayerSecrets/PlayerSecrets", () => ({
  default: vi.fn(() => null),
}));
vi.mock("../PlayerSets/PlayerSets", () => ({ default: vi.fn(() => null) }));
vi.mock("../../containers/DraftPile/DraftPileContainer", () => ({
  default: vi.fn(() => null),
}));

const MockPlayerHandContainer = vi.fn(() => (
  <div data-testid="mock-player-hand">Mock Hand</div>
));

const testGameId = "game-123";
const playerId = 2;
const jugadores = [
  { id_jugador: 2, nombre: "Pedro", posicionTurno: 1 },
  { id_jugador: 3, nombre: "María", posicionTurno: 2 },
  { id_jugador: 5, nombre: "Juan", posicionTurno: 3 },
];
const turnoActual = { id_jugador: 2, nombre: "Pedro", posicionTurno: 1 };
const discardPile = [];

const defaultAllSets = [
  { player_id: 2, sets: [] },
  { player_id: 3, sets: [] },
  { player_id: 5, sets: [] },
];

function renderComponent(props = {}) {
  render(
    <GameTable
      jugadores={jugadores}
      turnoActual={turnoActual}
      playerHand={[]}
      discardPile={discardPile}
      drawPile={[]}
      playerId={playerId}
      gameId={testGameId}
      PlayerHandContainer={MockPlayerHandContainer}
      allSets={defaultAllSets}
      {...props}
    />
  );
}

describe("GameTable", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    MockPlayerHandContainer.mockClear();
  });

  const setup = async (props = {}) => {
    renderComponent(props);

    await waitFor(() => {
      expect(MockPlayerHandContainer).toHaveBeenCalled();
    });
  };

  it("renders all player names", async () => {
    await setup();

    const MockPlayerInfo = (await import("../PlayerInfo/PlayerInfo")).default;
    await waitFor(() => {
      expect(MockPlayerInfo).toHaveBeenCalledTimes(3);
    });

    const nombres = ["Pedro", "María", "Juan"];

    nombres.forEach((nombre) => {
      expect(MockPlayerInfo).toHaveBeenCalledWith(
        expect.objectContaining({
          jugador: expect.objectContaining({ nombre }),
        }),
        undefined
      );
    });
  });

  it('renders the "Next turn" box with correct player name', async () => {
    await setup();

    expect(await screen.findByText("Next turn")).toBeInTheDocument();

    expect(screen.getByText("María")).toBeInTheDocument();
  });

  it('shows "Not available" if there are no players', async () => {
    await setup({ jugadores: [], turnoActual: null, allSets: [] });

    expect(await screen.findByText("Next turn")).toBeInTheDocument();
    expect(screen.getByText("Not available")).toBeInTheDocument();
  });

  it('shows "Not available" if turnoActual is missing', async () => {
    await setup({ turnoActual: null });

    expect(await screen.findByText("Next turn")).toBeInTheDocument();
    expect(screen.getByText("Not available")).toBeInTheDocument();
  });
});
