import { describe, it, expect, vi, beforeEach } from "vitest";
import { earlyTrainHandler } from "./EarlyTrainToPaddingtonHandler";

vi.mock("react-hot-toast", () => {
  const toastFn = vi.fn();
  toastFn.success = vi.fn();
  toastFn.remove = vi.fn();
  return { __esModule: true, default: toastFn };
});

// Luego importamos el mock
import toast from "react-hot-toast";

describe("earlyTrainHandler", () => {
  let payload, players, playerId;

  beforeEach(() => {
    vi.clearAllMocks();

    payload = {
      player_id: 1,
      card_name: "Early Train to Paddington",
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
      "You played Early Train to Paddington. Six cards were discarded from the deck!",
    ],
    [
      "other",
      2,
      "normal",
      "Alice played Early Train to Paddington. Six cards were discarded from the deck!",
    ],
  ])(
    "earlyTrainHandler para %s jugador",
    (_, testPlayerId, toastType, expected) => {
      playerId = testPlayerId;

      earlyTrainHandler(payload, playerId, players);

      expect(toast.remove).toHaveBeenCalled();
      if (toastType === "success") {
        expect(toast.success).toHaveBeenCalledWith(expected);
      } else {
        expect(toast).toHaveBeenCalledWith(expected, { icon: "🚂" });
      }
    }
  );
});

