import { describe, it, expect, vi, beforeEach } from "vitest";
import { anotherVictimHandler } from "./AnotherVictimHandler";
import toast from "react-hot-toast";

vi.mock("react-hot-toast", () => {
  const fn = vi.fn();
  fn.success = vi.fn();
  fn.error = vi.fn();
  fn.remove = vi.fn();
  return { __esModule: true, default: fn };
});

describe("anotherVictimHandler", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("usa toast.error cuando el jugador que jugó no es el jugador actual", () => {
    const payload = { player_id: 1, card_name: "Another Victim" };
    const players = [
      { id_jugador: 1, nombre: "Alice" },
      { id_jugador: 2, nombre: "Bob" },
    ];
    const playerId = 2;

    anotherVictimHandler(payload, playerId, players);

    expect(toast.remove).toHaveBeenCalled();
    expect(toast.error).toHaveBeenCalledWith(
      "Alice played Another Victim and stole a set! They are now playing it.",
      { icon: "🦝" }
    );
  });

  it("usa toast.success cuando el jugador actual jugó la carta", () => {
    const payload = { player_id: 2, card_name: "Another Victim" };
    const players = [
      { id_jugador: 1, nombre: "Alice" },
      { id_jugador: 2, nombre: "Bob" },
    ];
    const playerId = 2;

    anotherVictimHandler(payload, playerId, players);

    expect(toast.remove).toHaveBeenCalled();
    expect(toast.success).toHaveBeenCalledWith(
      "You played Another Victim and stole a set! Now you’re playing it."
    );
  });
});
