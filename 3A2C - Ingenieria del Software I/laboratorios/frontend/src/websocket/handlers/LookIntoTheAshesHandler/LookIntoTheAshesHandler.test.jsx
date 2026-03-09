import { describe, it, expect, vi, beforeEach } from "vitest";
import { lookIntoTheAshesHandler } from "./LookIntoTheAshesHandler";

vi.mock("react-hot-toast", () => {
  const toastFn = vi.fn();
  toastFn.success = vi.fn();
  toastFn.remove = vi.fn();
  return { __esModule: true, default: toastFn };
});

import toast from "react-hot-toast";

describe("lookIntoTheAshesHandler", () => {
  let payload, players, playerId;

  beforeEach(() => {
    vi.clearAllMocks();

    payload = {
      player_id: 1,
      card_name: "Look Into The Ashes",
      game_id: 123,
    };

    players = [
      { id_jugador: 1, nombre: "Alice" },
      { id_jugador: 2, nombre: "Bob" },
    ];
  });

  it.each([
    [
      "actor",
      1,
      "success",
      "You played Look Into The Ashes! You took one card from the discard pile.",
    ],
    [
      "other",
      2,
      "normal",
      "Alice played Look Into The Ashes and took one card from the discard pile!",
    ],
  ])(
    "lookIntoTheAshesHandler para %s jugador",
    (_, testPlayerId, toastType, expected) => {
      playerId = testPlayerId;

      lookIntoTheAshesHandler(payload, playerId, players);

      expect(toast.remove).toHaveBeenCalled();

      if (toastType === "success") {
        expect(toast.success).toHaveBeenCalledWith(expected);
      } else {
        expect(toast).toHaveBeenCalledWith(expected, { icon: "🦝" });
      }
    }
  );

  it("no hace nada si payload es null o undefined", () => {
    lookIntoTheAshesHandler(null, 1, players);
    expect(toast.remove).not.toHaveBeenCalled();
    expect(toast.success).not.toHaveBeenCalled();
    expect(toast).not.toHaveBeenCalled();
  });
});
