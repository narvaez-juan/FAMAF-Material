import { describe, test, expect, vi, beforeEach } from "vitest";
import React from "react";
import {
  render,
  screen,
  waitFor,
  fireEvent,
  act,
} from "@testing-library/react";
import "@testing-library/jest-dom";
import DraftPileContainer from "./DraftPileContainer";

//NOTES - Fixtures
const playerId = "test-player-id";
const playerFixture = { player_id: playerId, playerTurn: 1 };
const draftPileFixture = [
  { gameCardId: 101, image: "img1.png" },
  { gameCardId: 102, image: "img2.png" },
];
const gameInfoFixture = (turn = 1) => ({
  currentTurn: turn,
  players: [playerFixture],
});
const draftStateFixture = (cards = draftPileFixture) => ({
  draft_cards: cards,
});

//NOTES - Mocks
vi.mock("react-router-dom", () => ({
  useParams: () => ({ gameId: "test-game-id" }),
}));

vi.mock("../../components/DraftPile/DraftPileComponent", () => ({
  default: ({ draftPile, selectedCards, handleCardClick, loading }) => (
    <div>
      {loading && <span data-testid="loading">Cargando draft...</span>}
      {draftPile.length === 0 && !loading && (
        <span data-testid="empty">No hay cartas en draft.</span>
      )}
      {draftPile.map((card) => (
        <div
          key={card.gameCardId}
          data-testid="card"
          className={selectedCards.includes(card.gameCardId) ? "selected" : ""}
          onClick={() => handleCardClick(card.gameCardId)}
        >
          {card.gameCardId}
        </div>
      ))}
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

function getHandlers() {
  const draftHandler = mockSocket.on.mock.calls.find(
    (c) => c[0] === "draft_piles"
  )?.[1];
  const gameInfoHandler = mockSocket.on.mock.calls.find(
    (c) => c[0] === "game_info"
  )?.[1];
  return { draftHandler, gameInfoHandler };
}

describe("DraftPileContainer", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockSocket.on.mockClear();
    mockSocket.emit.mockClear();
  });

  test("renders cards from draft pile", async () => {
    render(<DraftPileContainer playerId={playerId} />);
    await waitFor(() => {
      expect(mockSocket.on).toHaveBeenCalledWith(
        "draft_piles",
        expect.any(Function)
      );
      expect(mockSocket.on).toHaveBeenCalledWith(
        "game_info",
        expect.any(Function)
      );
    });

    const { draftHandler, gameInfoHandler } = getHandlers();
    expect(draftHandler).toBeInstanceOf(Function);
    expect(gameInfoHandler).toBeInstanceOf(Function);

    act(() => {
      gameInfoHandler(gameInfoFixture(1));
      draftHandler(draftStateFixture());
    });

    await waitFor(() => {
      const cards = screen.getAllByTestId("card");
      expect(cards).toHaveLength(2);
      expect(cards[0]).toHaveTextContent("101");
      expect(cards[1]).toHaveTextContent("102");
    });
  });

  test("allows selection of cards when it's my turn", async () => {
    render(<DraftPileContainer playerId={playerId} />);
    await waitFor(() => {
      expect(mockSocket.on).toHaveBeenCalledWith(
        "draft_piles",
        expect.any(Function)
      );
      expect(mockSocket.on).toHaveBeenCalledWith(
        "game_info",
        expect.any(Function)
      );
    });

    const { draftHandler, gameInfoHandler } = getHandlers();
    expect(draftHandler).toBeInstanceOf(Function);
    expect(gameInfoHandler).toBeInstanceOf(Function);

    act(() => {
      gameInfoHandler(gameInfoFixture(1));
      draftHandler(draftStateFixture());
    });

    const cards = await screen.findAllByTestId("card");
    fireEvent.click(cards[0]);
    expect(cards[0]).toHaveClass("selected");
  });

  test("does not allow selection when it's not my turn", async () => {
    render(<DraftPileContainer playerId={playerId} />);
    await waitFor(() => {
      expect(mockSocket.on).toHaveBeenCalledWith(
        "draft_piles",
        expect.any(Function)
      );
      expect(mockSocket.on).toHaveBeenCalledWith(
        "game_info",
        expect.any(Function)
      );
    });

    const { draftHandler, gameInfoHandler } = getHandlers();
    expect(draftHandler).toBeInstanceOf(Function);
    expect(gameInfoHandler).toBeInstanceOf(Function);

    act(() => {
      gameInfoHandler(gameInfoFixture(2)); // No es mi turno
      draftHandler(draftStateFixture([{ gameCardId: 301, image: "img1.png" }]));
    });

    const card = await screen.findByTestId("card");
    fireEvent.click(card);
    expect(card).not.toHaveClass("selected");
  });

  test("deselects cards when turn changes", async () => {
    render(<DraftPileContainer playerId={playerId} />);
    await waitFor(() => {
      expect(mockSocket.on).toHaveBeenCalledWith(
        "draft_piles",
        expect.any(Function)
      );
      expect(mockSocket.on).toHaveBeenCalledWith(
        "game_info",
        expect.any(Function)
      );
    });

    const { draftHandler, gameInfoHandler } = getHandlers();
    expect(draftHandler).toBeInstanceOf(Function);
    expect(gameInfoHandler).toBeInstanceOf(Function);

    act(() => {
      gameInfoHandler(gameInfoFixture(1));
      draftHandler(draftStateFixture([{ gameCardId: 401, image: "img1.png" }]));
    });

    const card = await screen.findByTestId("card");
    fireEvent.click(card);
    expect(card).toHaveClass("selected");

    act(() => {
      gameInfoHandler(gameInfoFixture(2));
    });

    expect(card).not.toHaveClass("selected");
  });
});
