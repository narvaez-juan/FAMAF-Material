import { create } from "zustand";

export const useAnotherVictimStore = create((set) => ({
  selectPlayerToStealSet: false,
  selectSetToStealOpen: false,
  targetPlayerToStealSet: null,
  targetSetToStealId: null,
  newStolenSet: null,

  // Normal Setters
  setselectPlayerToStealSet: (val) => set({ selectPlayerToStealSet: val }),
  setSelectSetToStealOpen: (val) => set({ selectSetToStealOpen: val }),
  setNewStolenSet: (newset) => set({ newStolenSet: newset }),

  // Promise Setters
  setTargetPlayerToStealSet: (player) =>
    set((state) => {
      if (state._resolveTargetPromise) {
        state._resolveTargetPromise(player);
      }
      return {
        targetPlayerToStealSet: player,
        selectPlayerToStealSet: false,
        _resolveTargetPromise: null,
      };
    }),

  setTargetSetToStealId: (setId) =>
    set((state) => {
      if (state._resolveSetPromise) {
        state._resolveSetPromise(setId);
      }
      return {
        targetSetToStealId: setId,
        selectSetToStealOpen: false,
        _resolveSetPromise: null,
      };
    }),

  // Promise Section
  waitForTargetPlayerToStealSet: () =>
    new Promise((resolve) => {
      set({ _resolveTargetPromise: resolve, selectPlayerToStealSet: true });
    }),

  waitForTargetSetToStealId: () =>
    new Promise((resolve) => {
      set({ _resolveSetPromise: resolve, selectSetToStealOpen: true });
    }),
}));
