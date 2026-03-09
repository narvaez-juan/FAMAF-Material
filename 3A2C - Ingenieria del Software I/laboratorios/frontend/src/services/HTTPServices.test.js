import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { createHttpService } from "./HTTPServices";

describe("HTTPServices - createHttpService", () => {
  const originalFetch = global.fetch;

  beforeEach(() => {
    vi.resetAllMocks();
    global.fetch = vi.fn();
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  it("createGame should POST to /games/create and return json", async () => {
    const mockBody = { id: 123 };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockBody,
    });

    const svc = createHttpService();
    const payload = { name: "test" };
    const res = await svc.createGame(payload);

    expect(res).toEqual(mockBody);
    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(global.fetch).toHaveBeenCalledWith(
      "http://localhost:8000/games/create",
      expect.objectContaining({ method: "POST", body: JSON.stringify(payload) })
    );
  });

  it("getTurnInfo should GET /games/turn/:id and return json", async () => {
    const mockBody = { turn: 5 };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockBody,
    });

    const svc = createHttpService();
    const res = await svc.getTurnInfo(42);

    expect(res).toEqual(mockBody);
    expect(global.fetch).toHaveBeenCalledWith(
      "http://localhost:8000/games/turn/42",
      expect.objectContaining({ method: "GET" })
    );
  });

  it("startGame should POST to /games/:id/start with player_id", async () => {
    const mockBody = { started: true };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockBody,
    });

    const svc = createHttpService();
    const res = await svc.startGame(7, 99);

    expect(res).toEqual(mockBody);
    expect(global.fetch).toHaveBeenCalledWith(
      "http://localhost:8000/games/7/start",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ player_id: 99 }),
      })
    );
  });

  it("discardCard should POST card_ids array to /games/:gameId/discard/:playerId", async () => {
    const mockBody = { ok: true };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockBody,
    });

    const svc = createHttpService();
    const res = await svc.discardCard(8, 2, ["10", 11]);

    expect(res).toEqual(mockBody);
    expect(global.fetch).toHaveBeenCalledWith(
      "http://localhost:8000/games/8/discard/2",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ card_ids: [10, 11] }),
      })
    );
  });

  it("drawCard should POST payload to /games/:id/draw_card", async () => {
    const mockBody = { drawn: 2 };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockBody,
    });

    const svc = createHttpService();
    const res = await svc.drawCard(3, 4, [1, 2], 0);

    expect(res).toEqual(mockBody);
    expect(global.fetch).toHaveBeenCalledWith(
      "http://localhost:8000/games/3/draw_card",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({
          player_id: 4,
          draftCardsSelectedIds: [1, 2],
          drawPileSelectedCount: 0,
        }),
      })
    );
  });

  it("joinGame should POST to /games/:id/join with player data", async () => {
    const mockBody = { joined: true };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockBody,
    });

    const svc = createHttpService();
    const res = await svc.joinGame("Paco", "1990-01-01", 5);

    expect(res).toEqual(mockBody);
    expect(global.fetch).toHaveBeenCalledWith(
      "http://localhost:8000/games/5/join",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ player_name: "Paco", player_dob: "1990-01-01" }),
      })
    );
  });

  it("finishTurn should POST to /games/:id/turn with player_id", async () => {
    const mockBody = { ok: true };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockBody,
    });

    const svc = createHttpService();
    const res = await svc.finishTurn(11, 77);

    expect(res).toEqual(mockBody);
    expect(global.fetch).toHaveBeenCalledWith(
      "http://localhost:8000/games/11/turn",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ player_id: 77 }),
      })
    );
  });

  it("earlyTrainToPaddington should POST to /games/play/early-train-to-paddington/:gameId", async () => {
    const mockBody = { ok: true };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockBody,
    });

    const svc = createHttpService();
    const res = await svc.earlyTrainToPaddington(10, 20, 651);

    expect(res).toEqual(mockBody);
    expect(global.fetch).toHaveBeenCalledWith(
      "http://localhost:8000/games/play/early-train-to-paddington/10",
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          player_id: 20,
          id_early_train_to_paddington: 651,
        }),
      })
    );
  });


  it("should throw an Error with status when response.ok is false", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({}),
    });

    const svc = createHttpService();

    await expect(svc.getTurnInfo(1)).rejects.toMatchObject({
      message: "HTTP error",
      status: 500,
    });
  });

  it("should propagate network errors from fetch", async () => {
    const networkErr = new Error("network down");
    global.fetch.mockRejectedValueOnce(networkErr);

    const svc = createHttpService();

    await expect(svc.getTurnInfo(2)).rejects.toThrow("network down");
  });
});
