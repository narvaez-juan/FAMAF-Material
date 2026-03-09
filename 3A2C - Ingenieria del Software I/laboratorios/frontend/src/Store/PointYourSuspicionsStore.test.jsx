import { describe, it, vi, expect, beforeEach } from "vitest";
import playPointYourSuspicions from "../hooks/Card/EventCard/PointYourSuspicions/PointYourSuspicionsContainer";

// --- Módulos mockeados ---
import { useEventCardStore } from "./useEventCardStore";
import { usePointYourSuspicionsStore } from "./PointYourSuspicionsStore";
import { createHttpService } from "../services/HTTPServices";
import * as CardEmitter from "../websocket/emitters/CardEmitter"; // 👈 cambio clave

// --- Mocks ---
vi.mock("./useEventCardStore", () => {
  const getState = vi.fn();
  return { useEventCardStore: Object.assign(vi.fn(), { getState }) };
});

vi.mock("./PointYourSuspicionsStore", () => {
  const getState = vi.fn();
  return { usePointYourSuspicionsStore: Object.assign(vi.fn(), { getState }) };
});

vi.mock("../services/HTTPServices", () => ({
  createHttpService: vi.fn(),
}));

vi.mock("../websocket/emitters/CardEmitter", () => ({
  emitSelectPlayer: vi.fn(),
}));

// --- Test Suite ---
describe("playPointYourSuspicions", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("ejecuta correctamente todo el flujo del evento Point Your Suspicions", async () => {
    // --- Mock de funciones del store ---
    const waitForAllPlayersSelected = vi
      .fn()
      .mockResolvedValue([
        { target_player_id: "p2" },
        { target_player_id: "p3" },
      ]);
    const setPlayerId = vi.fn();
    const setExpectedPlayers = vi.fn();
    const clearSelectedPlayers = vi.fn();
    const clearEventCardClicked = vi.fn();

    usePointYourSuspicionsStore.getState.mockReturnValue({
      waitForAllPlayersSelected,
      setPlayerId,
      setExpectedPlayers,
      clearSelectedPlayers,
    });

    useEventCardStore.getState.mockReturnValue({
      clearEventCardClicked,
    });

    const pointYourSuspicionsMock = vi.fn().mockResolvedValue({});
    createHttpService.mockReturnValue({
      pointYourSuspicions: pointYourSuspicionsMock,
    });

    // --- Datos de prueba ---
    const card = { id: "event123", name: "Point Your Suspicions" };
    const context = { gameId: "game1", playerId: "p1", playersNumber: 3 };

    // --- Ejecutar función ---
    await playPointYourSuspicions(card, context);

    // --- Validaciones ---
    expect(setPlayerId).toHaveBeenCalledWith("p1");
    expect(setExpectedPlayers).toHaveBeenCalledWith(3);

    expect(CardEmitter.emitSelectPlayer).toHaveBeenCalledWith(
      "game1",
      "p1",
      "Point Your Suspicions",
      "Point Your Suspicions",
      "Event"
    );

    expect(waitForAllPlayersSelected).toHaveBeenCalledWith(3);

    expect(pointYourSuspicionsMock).toHaveBeenCalledWith(
      "game1",
      "p1",
      "event123",
      ["p2", "p3"]
    );

    expect(clearSelectedPlayers).toHaveBeenCalled();
    expect(clearEventCardClicked).toHaveBeenCalled();
  });

  it("no hace nada si no hay carta", async () => {
    const result = await playPointYourSuspicions(null, {
      gameId: "game1",
      playerId: "p1",
      playersNumber: 3,
    });

    expect(result).toEqual({});
    expect(CardEmitter.emitSelectPlayer).not.toHaveBeenCalled(); // 👈 corregido
  });
});
