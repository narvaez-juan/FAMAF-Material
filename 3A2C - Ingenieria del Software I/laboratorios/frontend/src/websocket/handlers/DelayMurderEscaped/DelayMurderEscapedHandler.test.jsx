import { describe, it, vi, beforeEach, expect } from "vitest";
import { delayMurderEscapedHandler } from "./DelayMurderEscapedHandler";
import toast from "react-hot-toast";

vi.mock("react-hot-toast", () => {
  const fn = vi.fn();
  fn.success = vi.fn();
  fn.remove = vi.fn();
  return { __esModule: true, default: fn };
});

describe("delayMurderEscapedHandler", () => {
  let payload, players, playerId;

  beforeEach(() => {
    vi.clearAllMocks();

    payload = { player_id: 1, card_name: "Delay Murder Escaped", game_id: 10 };
    players = [
      { id_jugador: 1, nombre: "Alice" },
      { id_jugador: 2, nombre: "Bob" },
    ];
    playerId = 1;
  });

  it.each([
    [
      "jugador actual",
      1,
      "success",
      "You played Delay Murder Escaped. Five cards were moved from the discard pile to the draw pile!",
    ],
    [
      "otro jugador",
      2,
      "normal",
      "Alice played Delay Murder Escaped. Five cards from the discard pile were moved to the draw pile!",
    ],
  ])(
    "muestra toast correcto cuando %s juega la carta",
    (_, testPlayerId, toastType, expectedMessage) => {
      playerId = testPlayerId;

      delayMurderEscapedHandler(payload, playerId, players);

      expect(toast.remove).toHaveBeenCalled();

      if (toastType === "success") {
        expect(toast.success).toHaveBeenCalledWith(expectedMessage);
      } else {
        expect(toast).toHaveBeenCalledWith(expectedMessage, { icon: "🐌" });
      }
    }
  );

  it("usa 'Unknown' si el jugador no está en la lista", () => {
    payload.player_id = 99;
    playerId = 2;

    delayMurderEscapedHandler(payload, playerId, players);

    expect(toast).toHaveBeenCalledWith(
      "Unknown played Delay Murder Escaped. Five cards from the discard pile were moved to the draw pile!",
      { icon: "🐌" }
    );
  });
});
