import { describe, test, expect, vi, beforeEach } from "vitest";
import {
  render,
  screen,
  waitFor,
  fireEvent,
  act,
} from "@testing-library/react";
import "@testing-library/jest-dom";
import PlayerHandContainer from "./PlayerHandContainer";

//SECTION - Mocks

vi.mock("react-router-dom", () => ({
  useParams: () => ({ gameId: "test-game-id" }),
}));

vi.mock("../../components/Card/Card", () => ({
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

const mockSocket = {
  emit: vi.fn(),
  on: vi.fn(),
  off: vi.fn(),
  connected: true,
};
vi.mock("../../services/WSServices", () => ({
  default: vi.fn(() => Promise.resolve(mockSocket)),
}));

const mockHttpService = {
  discardCard: vi.fn(() => Promise.resolve({})),
  stealSet: vi.fn(() => Promise.resolve({ success: true })),
};
vi.mock("../../services/HTTPServices", () => ({
  createHttpService: vi.fn(() => mockHttpService),
}));

const mockFinishTurn = vi.fn(() => Promise.resolve());
vi.mock("../GameLogic/FinishTurnContainer.jsx", () => ({
  default: () => ({
    finish: mockFinishTurn,
    loading: false,
    error: null,
  }),
}));

const mockDrawCard = vi.fn(() => Promise.resolve());
vi.mock("../GameLogic/DrawCardContainer.jsx", () => ({
  default: vi.fn(() => mockDrawCard),
}));

const mockPlaySet = vi.fn(() =>
  Promise.resolve({ message: { id: 1, effect: "Test" } })
);
const mockFetchPlayerSets = vi.fn(() => Promise.resolve());
let mockRequestedPlayerSets = [];
let mockIsLoadingSets = false;

vi.mock("../GameLogic/PlaySetContainer.jsx", () => ({
  default: () => ({
    allSets: [],
    get requestedPlayerSets() {
      return mockRequestedPlayerSets;
    },
    selectRequest: null,
    fetchPlayerSets: mockFetchPlayerSets,
    playSet: mockPlaySet,
    get isLoadingSets() {
      return mockIsLoadingSets;
    },
    error: null,
  }),
}));

vi.mock("../Game/GameRoomContainer.jsx", () => ({
  default: () => ({
    jugadores: [
      { id_jugador: "player-1", nombre: "Player 1", playerTurn: 0 },
      { id_jugador: "player-2", nombre: "Player 2", playerTurn: 1 },
    ],
    actualTurn: 0,
    inCourse: true,
  }),
}));

vi.mock("../Game/GameNotificationsContainer.jsx", () => ({
  default: () => ({
    emitWaitingModals: vi.fn(),
    secretNotification: null,
    emitSecretResolved: vi.fn(),
    selectSecretRequest: null,
  }),
}));

vi.mock("../../components/Modals/SelectSecretCard.jsx", () => ({
  default: () => <div data-testid="secret-modal">Secret Modal</div>,
}));

vi.mock("../../components/Modals/SelectPlayer.jsx", () => ({
  default: () => (
    <div data-testid="select-player-modal">Select Player Modal</div>
  ),
}));

vi.mock("../../components/Modals/WaitingModal.jsx", () => ({
  default: () => <div data-testid="waiting-modal">Waiting Modal</div>,
}));

vi.mock("../../components/Modals/SelectPlayerForSets.jsx", () => ({
  default: ({ onConfirm, onCancel }) => (
    <div data-testid="select-steal-target-modal">
      <button
        onClick={() =>
          onConfirm({ id_jugador: "player-2", nombre: "Player 2" })
        }
      >
        Select Player 2
      </button>
      <button onClick={onCancel}>Cancel</button>
    </div>
  ),
}));

vi.mock("../../components/Modals/SelectSetToStealModal.jsx", () => ({
  default: ({ sets, onConfirm, onCancel }) => (
    <div data-testid="select-set-to-steal-modal">
      {sets.map((set) => (
        <button
          key={set.set_play_id}
          onClick={() => onConfirm(set.set_play_id)}
        >
          Steal Set {set.set_play_id}
        </button>
      ))}
      <button onClick={onCancel}>Cancel</button>
    </div>
  ),
}));
//!SECTION

describe("PlayerHandContainer (Logic)", () => {
  const playerId = "test-player-id";
  const mockSetDiscardedCount = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    mockSocket.on.mockClear();
    mockSocket.emit.mockClear();
    mockSetDiscardedCount.mockClear();
    mockFetchPlayerSets.mockClear();
    mockHttpService.stealSet.mockClear();
    mockRequestedPlayerSets = [];
    mockIsLoadingSets = false;
  });

  test("Should discard the selected cards", async () => {
    render(
      <PlayerHandContainer
        playerId={playerId}
        setDiscardedCount={mockSetDiscardedCount}
      />
    );

    let gameInfoHandler, handHandler;
    await waitFor(() => {
      const gameInfoCall = mockSocket.on.mock.calls.find(
        (call) => call[0] === "game_info"
      );
      expect(gameInfoCall).toBeDefined();
      gameInfoHandler = gameInfoCall[1];

      const handCall = mockSocket.on.mock.calls.find(
        (call) => call[0] === "initial_hand"
      );
      expect(handCall).toBeDefined();
      handHandler = handCall[1];
    });

    act(() => {
      gameInfoHandler({
        currentTurn: 1,
        players: [{ player_id: playerId, playerTurn: 1 }],
      });
      handHandler({
        player_id: playerId,
        cards_list: [{ gameCardId: 136, card_id: 9, image: "img.png" }],
      });
    });

    const card = await screen.findByTestId("card");
    fireEvent.click(card);

    const discardButton = await screen.findByText("Discard (1)");
    await waitFor(() => {
      expect(discardButton).not.toBeDisabled();
    });
    fireEvent.click(discardButton);

    await waitFor(() => {
      expect(mockHttpService.discardCard).toHaveBeenCalledWith(
        "test-game-id",
        playerId,
        [136]
      );
    });
  });

  test("should handle finish turn correctly", async () => {
    render(
      <PlayerHandContainer
        playerId={playerId}
        setDiscardedCount={mockSetDiscardedCount}
        selectedDraftCards={[]}
        setSelectedDraftCards={vi.fn()}
        selectedDrawCardsNumber={0}
        setSelectedDrawCardsNumber={vi.fn()}
      />
    );

    let gameInfoHandler;
    await waitFor(() => {
      gameInfoHandler = mockSocket.on.mock.calls.find(
        (c) => c[0] === "game_info"
      )?.[1];
      expect(gameInfoHandler).toBeDefined();
      gameInfoHandler = mockSocket.on.mock.calls.find(
        (c) => c[0] === "game_info"
      )?.[1];
      expect(gameInfoHandler).toBeDefined();
    });

    act(() => {
      gameInfoHandler({
        currentTurn: 1,
        players: [{ player_id: playerId, playerTurn: 1 }],
      });
    });

    await waitFor(() => {
      const finishButton = screen.getByText("End Turn(60)");
      expect(finishButton).not.toBeDisabled();
      fireEvent.click(finishButton);
    });

    await waitFor(() => {
      expect(mockFinishTurn).toHaveBeenCalledWith(
        "test-game-id",
        playerId,
        false,
        false,
        [],
        6
      );
    });
  });

  test("buttons should be disabled when it is not my turn", async () => {
    render(
      <PlayerHandContainer
        playerId={playerId}
        setDiscardedCount={mockSetDiscardedCount}
      />
    );

    let gameInfoHandler, handHandler;
    await waitFor(() => {
      gameInfoHandler = mockSocket.on.mock.calls.find(
        (c) => c[0] === "game_info"
      )[1];
      handHandler = mockSocket.on.mock.calls.find(
        (c) => c[0] === "initial_hand"
      )[1];
    });

    act(() => {
      gameInfoHandler({
        currentTurn: 2, // No es mi turno
        players: [{ player_id: playerId, playerTurn: 1 }],
      });
      handHandler({
        player_id: playerId,
        cards_list: [{ gameCardId: 1, card_id: 1, image: "img.png" }],
      });
    });

    await screen.findByTestId("card");

    expect(screen.getByText("Discard (0)")).toBeDisabled();
    expect(screen.getByText("End Turn(60)")).toBeDisabled();
  });
});
