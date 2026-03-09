import { describe, it, expect, beforeEach } from "vitest";
import { intoTheAshesStore } from "./IntoTheAshesStore";

describe("intoTheAshesStore", () => {
  beforeEach(() => {
    intoTheAshesStore.setState({
      openModalByIntoTheAshes: false,
      selectedCardToDraw: null,
      _resolveSelectedCardToDrawPromise: null,
    });
  });

  it("setOpenModal actualiza correctamente el estado", () => {
    intoTheAshesStore.getState().setOpenModal(true);
    expect(intoTheAshesStore.getState().openModalByIntoTheAshes).toBe(true);

    intoTheAshesStore.getState().setOpenModal(false);
    expect(intoTheAshesStore.getState().openModalByIntoTheAshes).toBe(false);
  });

  it("waitForSelectedCardToDraw crea una promesa que se resuelve con setSelectedCardToDraw", async () => {
    const promise = intoTheAshesStore.getState().waitForSelectedCardToDraw();

    expect(
      intoTheAshesStore.getState()._resolveSelectedCardToDrawPromise
    ).toBeTypeOf("function");

    intoTheAshesStore.getState().setSelectedCardToDraw("card_123");

    const resolved = await promise;
    expect(resolved).toBe("card_123");

    const state = intoTheAshesStore.getState();
    expect(state.selectedCardToDraw).toBe("card_123");
    expect(state._resolveSelectedCardToDrawPromise).toBeNull();
  });
});
