import { describe, it, expect, vi, beforeEach } from "vitest";
import { offTheTableHandler } from "./CardsOfTheTableHandler";
import toast from "react-hot-toast";

vi.mock("react-hot-toast", () => {
  const fn = vi.fn(); // la función toast()
  fn.error = vi.fn(); // toast.error()
  fn.remove = vi.fn(); // toast.remove()
  return { __esModule: true, default: fn };
});

describe("offTheTableHandler", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("usa toast.error cuando el target es el jugador actual", () => {
    const payload = {
      player_id: 1,
      target_player_id: 2,
      card_name: "Cards Off The Table",
    };
    const players = [
      { id_jugador: 1, nombre: "Alice" },
      { id_jugador: 2, nombre: "Bob" },
    ];
    const playerId = 2;

    offTheTableHandler(payload, playerId, players);

    expect(toast.remove).toHaveBeenCalled();
    expect(toast.error).toHaveBeenCalledWith(
      "Alice played Cards Off The Table against you! You lose all your Not So Fast cards."
    );
  });

  it("usa toast normal cuando el target es otro jugador", () => {
    const payload = {
      player_id: 1,
      target_player_id: 2,
      card_name: "Cards Off The Table",
    };
    const players = [
      { id_jugador: 1, nombre: "Alice" },
      { id_jugador: 2, nombre: "Bob" },
    ];
    const playerId = 1;

    offTheTableHandler(payload, playerId, players);

    expect(toast.remove).toHaveBeenCalled();
    expect(toast).toHaveBeenCalledWith(
      "Alice played Cards Off The Table against Bob. Bob loses all their Not So Fast cards."
    );
  });
});
