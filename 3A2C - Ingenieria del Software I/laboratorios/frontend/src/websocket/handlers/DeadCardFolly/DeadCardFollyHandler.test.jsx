import { describe, it, vi, beforeEach, expect } from "vitest";
import {
  handleSelectCardPayload,
  handleSelectCardResolve,
  deadCardFollyHandler,
} from "./DeadCardFollyHandler";
import { useEventCardStore } from "../../../Store/useEventCardStore";
import { useDeadCardFollyStore } from "../../../Store/DeadCardFollyStore";
import toast from "react-hot-toast";

vi.mock("react-hot-toast", () => {
  const fn = vi.fn();
  fn.success = vi.fn();
  fn.remove = vi.fn();
  fn.dismiss = vi.fn();
  return { __esModule: true, default: fn };
});

vi.mock("../../../Store/useEventCardStore", () => ({
  useEventCardStore: {
    getState: vi.fn(),
  },
}));

vi.mock("../../../Store/DeadCardFollyStore", () => ({
  useDeadCardFollyStore: {
    getState: vi.fn(),
  },
}));

describe("DeadCardFollyHandler", () => {
  let payload, players, playerId;

  beforeEach(() => {
    vi.clearAllMocks();

    payload = { player_id: 1, card_name: "Dead Card Folly", game_id: 123 };
    players = [
      { id_jugador: 1, nombre: "Alice" },
      { id_jugador: 2, nombre: "Bob" },
    ];
    playerId = 1;

    // Mock por defecto
    useDeadCardFollyStore.getState.mockReturnValue({
      setSelectCardInfo: vi.fn(),
      setSelectCard: vi.fn(),
      setSelectedCardsByPlayers: vi.fn(),
    });
  });

  it("handleSelectCardPayload llama a setSelectCardInfo y setSelectCard", () => {
    const setSelectCardInfo = vi.fn();
    const setSelectCard = vi.fn();
    useDeadCardFollyStore.getState.mockReturnValue({
      setSelectCardInfo,
      setSelectCard,
    });

    handleSelectCardPayload(payload);

    expect(setSelectCardInfo).toHaveBeenCalledWith(payload);
    expect(setSelectCard).toHaveBeenCalledWith(true);
  });

  it("handleSelectCardResolve llama a setSelectedCardsByPlayers", () => {
    const setSelectedCardsByPlayers = vi.fn();
    useDeadCardFollyStore.getState.mockReturnValue({
      setSelectedCardsByPlayers,
    });

    const selected = [{ player_id: 1, card_id: 2 }];
    handleSelectCardResolve(selected);

    expect(setSelectedCardsByPlayers).toHaveBeenCalledWith(selected);
  });

  it("deadCardFollyHandler muestra toast.success cuando el jugador es el actor", () => {
    playerId = 1;

    deadCardFollyHandler(payload, playerId, players);

    expect(toast.success).toHaveBeenCalledWith(
      "you played Dead Card Folly successfully!. All players passed one card.",
      { id: "dead-card-folly-1" }
    );
  });

  it("deadCardFollyHandler muestra toast normal cuando el jugador NO es el actor", () => {
    playerId = 2;

    deadCardFollyHandler(payload, playerId, players);

    expect(toast).toHaveBeenCalledWith(
      "Alice played Dead Card Folly! All players passed one card.",
      {
        icon: "🧙‍♂️",
        id: "dead-card-folly-1",
      }
    );
  });
});
