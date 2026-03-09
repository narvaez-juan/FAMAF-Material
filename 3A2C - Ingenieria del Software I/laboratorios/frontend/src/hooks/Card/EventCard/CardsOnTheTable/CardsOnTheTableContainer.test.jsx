import { describe, it, vi, expect, beforeEach } from "vitest";
import useCardsOnTheTable from "./CardsOnTheTableContainer";
import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { createHttpService } from "../../../../services/HTTPServices";

vi.mock("../../../../Store/useEventCardStore", () => ({
  useEventCardStore: {
    getState: vi.fn(),
  },
}));

vi.mock("../../../../services/HTTPServices", () => ({
  createHttpService: vi.fn(),
}));

describe("useCardsOnTheTable", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("llama al flujo correcto (store + http service)", async () => {
    // Mock del store
    const setSelectPlayer = vi.fn();
    const waitForTargetPlayer = vi.fn().mockResolvedValue({ id: "target123" });
    const eventCardClicked = { id: "card999" };

    useEventCardStore.getState.mockReturnValue({
      setSelectPlayer,
      waitForTargetPlayer,
      eventCardClicked,
      clearEventCardClicked: vi.fn(),
    });

    // Mock del servicio HTTP
    const cardsOfTheTable = vi.fn().mockResolvedValue({});
    createHttpService.mockReturnValue({ cardsOfTheTable });

    // Datos de prueba
    const card = { id: "card999", name: "cards on the table" };
    const context = { gameId: "game123", playerId: "player456" };

    // Ejecutar el hook
    await useCardsOnTheTable(card, context);

    // Verificaciones
    expect(setSelectPlayer).toHaveBeenCalledWith(true);
    expect(waitForTargetPlayer).toHaveBeenCalled();
    expect(cardsOfTheTable).toHaveBeenCalledWith(
      "game123",
      "player456",
      "card999",
      "target123"
    );
  });
});
