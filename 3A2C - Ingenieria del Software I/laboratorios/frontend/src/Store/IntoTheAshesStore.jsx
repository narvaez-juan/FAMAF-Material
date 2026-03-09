import { create } from "zustand";

export const intoTheAshesStore = create((set) => ({
  openModalByIntoTheAshes: false,
  selectedCardToDraw: null,

  // Setters
  setOpenModal: (val) => set({ openModalByIntoTheAshes: val }),

  // Promise Setters
  setSelectedCardToDraw: (card_id) =>
    set((state) => {
      if (state._resolveSelectedCardToDrawPromise) {
        state._resolveSelectedCardToDrawPromise(card_id);
      }
      return {
        selectedCardToDraw: card_id,
        _resolveSelectedCardToDrawPromise: null,
      };
    }),

  // Promise Section
  waitForSelectedCardToDraw: () =>
    new Promise((resolve) => {
      set({
        _resolveSelectedCardToDrawPromise: resolve,
      });
    }),
}));
