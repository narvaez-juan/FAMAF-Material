import { describe, it, expect, beforeEach } from "vitest";
import { delayMurderEscapesStore } from "./DelayMurderEscapesStore";

describe("delayMurderEscapesStore", () => {
  beforeEach(() => {
    delayMurderEscapesStore.setState({
      openDiscardModal: false,
      allDiscardCardSelected: [],
      _resolveDiscardCardPromise: null,
    });
  });

  it("setOpenDiscardModal cambia el estado correctamente", () => {
    delayMurderEscapesStore.getState().setOpenDiscardModal(true);
    expect(delayMurderEscapesStore.getState().openDiscardModal).toBe(true);
  });

  it("setAllDiscardCardSelected actualiza las cartas correctamente", () => {
    const cards = [{ id: 1, name: "Ace" }];
    delayMurderEscapesStore.getState().setAllDiscardCardSelected(cards);
    expect(delayMurderEscapesStore.getState().allDiscardCardSelected).toEqual(
      cards
    );
  });

  it("waitForDiscardCardSelection devuelve una promesa que se resuelve al llamar setAllDiscardCardSelected", async () => {
    const promise = delayMurderEscapesStore
      .getState()
      .waitForDiscardCardSelection();

    const initialState = delayMurderEscapesStore.getState();
    expect(initialState._resolveDiscardCardPromise).toBeTypeOf("function");

    const selectedCards = [{ id: 2, name: "King" }];
    delayMurderEscapesStore.getState().setAllDiscardCardSelected(selectedCards);

    const resolved = await promise;
    expect(resolved).toEqual(selectedCards);

    const state = delayMurderEscapesStore.getState();
    expect(state.allDiscardCardSelected).toEqual(selectedCards);
    expect(state._resolveDiscardCardPromise).toBeNull();
  });
});
