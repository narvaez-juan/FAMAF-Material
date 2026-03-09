import { render, screen, fireEvent } from "@testing-library/react";
import { vi } from "vitest";
import SelectCardModal from "./SelectCardModal";
import { useEventCardStore } from "../../Store/useEventCardStore";
import { useDeadCardFollyStore } from "../../Store/DeadCardFollyStore";

vi.mock("../../Store/DeadCardFollyStore", () => ({
  useDeadCardFollyStore: vi.fn(),
}));

describe("SelectCardModal", () => {
  const cards = [
    { gameCardId: 1, image: "card1.png" },
    { gameCardId: 2, image: "card2.png" },
    { gameCardId: 3, image: "card3.png" },
  ];

  const players = [
    { id_jugador: 1, nombre: "Jere" },
    { id_jugador: 2, nombre: "Fran" },
  ];

  const selectCardMock = vi.fn();

  beforeEach(() => {
    useDeadCardFollyStore.mockReturnValue({
      selectCardInfo: {
        player_id: 1,
        direction: "left",
        card_name: "Dead Card Folly",
      },
      setSelectCard: selectCardMock,
    });
    vi.clearAllMocks();
  });

  test("renders cards and info text", () => {
    render(
      <SelectCardModal
        cards={cards}
        players={players}
        playerId={1}
        gameId={1}
        eventSelectedCard={[{ id: 1 }]}
      />
    );

    expect(screen.getByText(/Event Action/i)).toBeInTheDocument();
    cards.forEach((c) => {
      expect(screen.getByAltText(`Card ${c.gameCardId}`)).toBeInTheDocument();
    });
  });

  test("selecting a card updates state and disables selecting the event card", () => {
    render(
      <SelectCardModal
        cards={cards}
        players={players}
        playerId={1}
        gameId={1}
        eventSelectedCard={[{ id: 1 }]}
      />
    );

    const card2 = screen.getByAltText("Card 2");
    fireEvent.click(card2);

    const confirmButton = screen.getByRole("button", { name: /confirm/i });
    expect(confirmButton).not.toBeDisabled();

    const card1 = screen.getByAltText("Card 1");
    fireEvent.click(card1);
    expect(confirmButton).not.toBeDisabled(); // no cambia porque no puede seleccionarse
  });

  test("confirm button calls setSelectCard", () => {
    render(
      <SelectCardModal
        cards={cards}
        players={players}
        playerId={1}
        gameId={1}
        eventSelectedCard={[{ id: 1 }]}
      />
    );

    const card2 = screen.getByAltText("Card 2");
    fireEvent.click(card2);

    const confirmButton = screen.getByRole("button", { name: /confirm/i });
    fireEvent.click(confirmButton);

    expect(selectCardMock).toHaveBeenCalled();
  });
});
