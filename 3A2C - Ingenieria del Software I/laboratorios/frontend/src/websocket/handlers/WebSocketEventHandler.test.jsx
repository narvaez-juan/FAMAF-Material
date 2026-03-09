import { describe, it, expect, vi, beforeEach } from "vitest";
import { handleGameEvent } from "./WebSocketEventHandler";
import * as CardsHandler from "./CardsOfTheTable/CardsOfTheTableHandler";
import * as deadCardFollyHandler from "./DeadCardFolly/DeadCardFollyHandler";
import * as EarlyTrainHandler from "./EarlyTrainToPaddington/EarlyTrainToPaddingtonHandler";
import * as PointHandler from "./PointYourSupcicions/PointYourSuspicionsHandler";

describe("handleGameEvent", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("llama a offTheTableHandler cuando card_name es 'Cards Off The Table'", () => {
    const mockHandler = vi
      .spyOn(CardsHandler, "offTheTableHandler")
      .mockImplementation(() => {});
    const payload = { card_name: "Cards Off The Table", game_id: 1 };
    const playerId = 123;
    const players = [{ id_jugador: 123, nombre: "Alice" }];

    handleGameEvent(payload, playerId, players);

    expect(mockHandler).toHaveBeenCalledWith(payload, playerId, players);
  });

  it("llama a console.warn para card_name desconocido", () => {
    const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});
    const payload = { card_name: "Unknown Card", game_id: 1 };
    const playerId = 123;
    const players = [{ id_jugador: 123, nombre: "Alice" }];

    handleGameEvent(payload, playerId, players);

    expect(warnSpy).toHaveBeenCalledWith("Unhandled event:", payload);
  });

  it("llama a deadCardFollyHandler cuando card_name es 'Dead Card Folly'", () => {
    const mockHandler = vi
      .spyOn(deadCardFollyHandler, "deadCardFollyHandler")
      .mockImplementation(() => {});
    const payload = { card_name: "Dead Card Folly", game_id: 1 };
    const playerId = 123;
    const players = [{ id_jugador: 123, nombre: "Alice" }];

    handleGameEvent(payload, playerId, players);

    expect(mockHandler).toHaveBeenCalledWith(payload, playerId, players);
  });

  it("no hace nada si payload es null o undefined", () => {
    const mockHandler = vi.spyOn(CardsHandler, "offTheTableHandler");
    const warnSpy = vi.spyOn(console, "warn");

    handleGameEvent(null, 1, []);
    handleGameEvent(undefined, 1, []);

    expect(mockHandler).not.toHaveBeenCalled();
    expect(warnSpy).not.toHaveBeenCalled();
  });

  it("llama a earlyTrainHandler cuando card_name es 'Early Train to Paddington'", () => {
    const mockHandler = vi
      .spyOn(EarlyTrainHandler, "earlyTrainHandler")
      .mockImplementation(() => {});
    const payload = { card_name: "Early Train to Paddington", game_id: 1 };
    const playerId = 123;
    const players = [{ id_jugador: 123, nombre: "Alice" }];

    handleGameEvent(payload, playerId, players);

    expect(mockHandler).toHaveBeenCalledWith(payload, playerId, players);
  });

  it("llama a PointYourSuspicionsHandler cuando card_name es 'Point Your Suspicion'", () => {
    const mockHandler = vi
      .spyOn(PointHandler, "PointYourSuspicionsHandler")
      .mockImplementation(() => {});
    const payload = { card_name: "Point Your Suspicion", game_id: 1 };
    const playerId = 123;
    const players = [{ id_jugador: 123, nombre: "Alice" }];

    handleGameEvent(payload, playerId, players);

    expect(mockHandler).toHaveBeenCalledWith(payload, playerId, players);
  });
});
