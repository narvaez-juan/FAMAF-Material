import { describe, it, expect, vi, beforeEach } from "vitest";
import { PointYourSuspicionsHandler } from "./PointYourSuspicionsHandler";
import { usePointYourSuspicionsStore } from "../../../Store/PointYourSuspicionsStore";
import { useEventCardStore } from "../../../Store/useEventCardStore";
import { emitSecrets } from "../../../services/WSServices";

// Mock del toast
vi.mock("react-hot-toast", () => {
  const toastFn = vi.fn();
  toastFn.success = vi.fn();
  toastFn.error = vi.fn();
  toastFn.remove = vi.fn();
  toastFn.dismiss = vi.fn();
  return { __esModule: true, default: toastFn };
});

import toast from "react-hot-toast";

// Mock del socket
vi.mock("../../../services/WSServices", () => ({
  emitSecrets: vi.fn(),
}));

// Mock del store PointYourSuspicions
vi.mock("../../../Store/PointYourSuspicionsStore", () => ({
  usePointYourSuspicionsStore: {
    getState: vi.fn(),
  },
}));

// Mock del store EventCard (IMPORTANTE: probablemente este es el que usa)
vi.mock("../../../Store/useEventCardStore", () => ({
  useEventCardStore: {
    getState: vi.fn(),
  },
}));

describe("PointYourSuspicionsHandler", () => {
  let payload, players, mockSetVotedToReveal, mockSetVotedPlayerId;

  beforeEach(() => {
    vi.clearAllMocks();

    mockSetVotedToReveal = vi.fn();
    mockSetVotedPlayerId = vi.fn();

    // Mock para PointYourSuspicionsStore
    usePointYourSuspicionsStore.getState.mockReturnValue({
      setVotedToReveal: mockSetVotedToReveal,
      setVotedPlayerId: mockSetVotedPlayerId,
    });

    // Mock para EventCardStore (probablemente el que realmente usa)
    useEventCardStore.getState.mockReturnValue({
      setVotedToReveal: mockSetVotedToReveal,
      setVotedPlayerId: mockSetVotedPlayerId,
      setSecrets: vi.fn(),
      secretsByPlayer: {},
    });

    payload = {
      player_id: 1,
      target_player_id: 2,
      card_name: "Point Your Suspicions",
      game_id: "G123",
    };

    players = [
      { id_jugador: 1, nombre: "Alice" },
      { id_jugador: 2, nombre: "Bob" },
      { id_jugador: 3, nombre: "Charlie" },
    ];
  });

  it("muestra toast.error y emite secretos si el jugador actual es el target", async () => {
    await PointYourSuspicionsHandler(payload, 2, players);

    expect(toast.remove).toHaveBeenCalled();
    expect(toast.error).toHaveBeenCalledWith(
      "Alice played Point Your Suspicions! You have been selected to reveal a secret!",
      { icon: "❗" }
    );
    expect(emitSecrets).toHaveBeenCalledWith("G123", 2);
    expect(mockSetVotedPlayerId).toHaveBeenCalledWith(2);
    expect(mockSetVotedToReveal).toHaveBeenCalledWith(true);
  });

  it("muestra toast.success si el jugador actual fue quien jugó la carta", async () => {
    await PointYourSuspicionsHandler(payload, 1, players);

    expect(toast.remove).toHaveBeenCalled();
    expect(toast.success).toHaveBeenCalledWith(
      "You played Point Your Suspicions! The group voted and Bob has been selected to reveal a secret."
    );
    expect(emitSecrets).not.toHaveBeenCalled();
  });

  it("muestra toast normal si el jugador actual es un observador", async () => {
    await PointYourSuspicionsHandler(payload, 3, players);

    expect(toast.remove).toHaveBeenCalled();
    expect(toast).toHaveBeenCalledWith(
      "Alice played Point Your Suspicions! The group voted and Bob has been selected to reveal a secret.",
      { icon: "🕵️" }
    );
    expect(emitSecrets).not.toHaveBeenCalled();
  });

  it("no hace nada si payload es null", async () => {
    await PointYourSuspicionsHandler(null, 1, players);

    expect(toast.remove).not.toHaveBeenCalled();
    expect(toast.success).not.toHaveBeenCalled();
    expect(toast.error).not.toHaveBeenCalled();
    expect(toast).not.toHaveBeenCalled();
    expect(emitSecrets).not.toHaveBeenCalled();
  });
});
