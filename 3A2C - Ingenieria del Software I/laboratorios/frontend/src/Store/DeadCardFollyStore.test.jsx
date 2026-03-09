import { describe, it, expect, beforeEach } from "vitest";
import { useDeadCardFollyStore } from "./DeadCardFollyStore";

describe("useDeadCardFollyStore", () => {
  beforeEach(() => {
    useDeadCardFollyStore.setState({
      selectCardInfo: null,
      selectCard: false,
      selectedCardsByPlayers: [],
      _expectedPlayers: 0,
      selectDirection: false,
      selectedDirection: "right",
      _resolveCardsPromise: null,
      _resolveDirectionPromise: null,
    });
  });

  it("setSelectCardInfo, setSelectCard y setSelectDirection actualizan correctamente", () => {
    useDeadCardFollyStore.getState().setSelectCardInfo({ id: 1 });
    expect(useDeadCardFollyStore.getState().selectCardInfo).toEqual({ id: 1 });

    useDeadCardFollyStore.getState().setSelectCard(true);
    expect(useDeadCardFollyStore.getState().selectCard).toBe(true);

    useDeadCardFollyStore.getState().setSelectDirection(true);
    expect(useDeadCardFollyStore.getState().selectDirection).toBe(true);
  });

  it("setSelectedDirection resuelve la promesa y actualiza el estado", async () => {
    const promise = useDeadCardFollyStore.getState().waitForDirection();

    expect(
      useDeadCardFollyStore.getState()._resolveDirectionPromise
    ).toBeTypeOf("function");
    expect(useDeadCardFollyStore.getState().selectDirection).toBe(true);

    useDeadCardFollyStore.getState().setSelectedDirection("left");

    const resolved = await promise;
    expect(resolved).toBe("left");

    const state = useDeadCardFollyStore.getState();
    expect(state.selectedDirection).toBe("left");
    expect(state._resolveDirectionPromise).toBeNull();
    expect(state.selectDirection).toBe(false);
  });

  it("waitForAllCardsSelected resuelve cuando todos los jugadores seleccionan carta", async () => {
    const totalPlayers = 2;
    const promise = useDeadCardFollyStore
      .getState()
      .waitForAllCardsSelected(totalPlayers);

    useDeadCardFollyStore.getState().setSelectedCardsByPlayers({
      player_id: "p1",
      card: "A",
    });
    expect(
      useDeadCardFollyStore.getState().selectedCardsByPlayers
    ).toHaveLength(1);

    useDeadCardFollyStore.getState().setSelectedCardsByPlayers({
      player_id: "p2",
      card: "B",
    });

    const resolved = await promise;
    expect(resolved).toEqual([
      { player_id: "p1", card: "A" },
      { player_id: "p2", card: "B" },
    ]);

    const state = useDeadCardFollyStore.getState();
    expect(state.selectedCardsByPlayers).toHaveLength(2);
  });

  it("setSelectedCardsByPlayers actualiza el jugador si ya existe", () => {
    useDeadCardFollyStore.setState({
      selectedCardsByPlayers: [{ player_id: "p1", card: "A" }],
    });

    useDeadCardFollyStore
      .getState()
      .setSelectedCardsByPlayers({ player_id: "p1", card: "K" });

    const updated = useDeadCardFollyStore.getState().selectedCardsByPlayers;
    expect(updated).toEqual([{ player_id: "p1", card: "K" }]);
  });
});
