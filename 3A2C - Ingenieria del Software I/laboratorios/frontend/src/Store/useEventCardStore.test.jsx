import { describe, it, expect, beforeEach } from "vitest";
import { useEventCardStore } from "./useEventCardStore";

describe("useEventCardStore", () => {
  beforeEach(() => {
    useEventCardStore.setState(
      useEventCardStore.getInitialState?.() ?? {
        eventCardClicked: null,
        selectPlayer: false,
        targetPlayer: null,
      }
    );
  });

  it("setSelectPlayer cambia el estado correctamente", () => {
    useEventCardStore.getState().setSelectPlayer(true);
    expect(useEventCardStore.getState().selectPlayer).toBe(true);
  });

  it("setEventCardClicked y clearEventCardClicked funcionan correctamente", () => {
    const card = { id: "c1", name: "test" };
    useEventCardStore.getState().setEventCardClicked(card);
    expect(useEventCardStore.getState().eventCardClicked).toEqual(card);

    useEventCardStore.getState().clearEventCardClicked();
    expect(useEventCardStore.getState().eventCardClicked).toBeNull();
  });

  it("waitForTargetPlayer devuelve una promesa que se resuelve al llamar setTargetPlayer", async () => {
    const promise = useEventCardStore.getState().waitForTargetPlayer();

    // esperando
    expect(useEventCardStore.getState().selectPlayer).toBe(true);

    // selecciona jugador
    const player = { id: "p1", name: "Alice" };
    useEventCardStore.getState().setTargetPlayer(player);

    // promesa
    const resolved = await promise;
    expect(resolved).toEqual(player);

    // selección
    const state = useEventCardStore.getState();
    expect(state.targetPlayer).toEqual(player);
    expect(state.selectPlayer).toBe(false);
  });
});
