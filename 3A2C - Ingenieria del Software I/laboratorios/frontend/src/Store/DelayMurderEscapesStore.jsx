import { create } from "zustand";

export const delayMurderEscapesStore = create((set) => ({
  openDiscardModal: false,
  allDiscardCardSelected: [],

  // Setters
  setOpenDiscardModal: (val) => set({ openDiscardModal: val }),

  // Promise Setters
  setAllDiscardCardSelected: (cards) =>
    set((state) => {
      if (state._resolveDiscardCardPromise) {
        state._resolveDiscardCardPromise(cards);
      }
      return {
        allDiscardCardSelected: cards,
        _resolveDiscardCardPromise: null,
      };
    }),

  // Promise Section
  waitForDiscardCardSelection: () =>
    new Promise((resolve) => {
      set({
        _resolveDiscardCardPromise: resolve,
      });
    }),
}));
