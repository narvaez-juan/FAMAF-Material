import { create } from "zustand";

export const useDeadCardFollyStore = create((set) => ({
  selectCardInfo: null,
  selectCard: false,
  selectedCardsByPlayers: [],
  _expectedPlayers: 0,
  selectDirection: false,
  selectedDirection: "right",

  // Setters
  setSelectCardInfo: (val) => set({ selectCardInfo: val }),
  setSelectCard: (val) => set({ selectCard: val }),
  setExpectedPlayers: (val) => set({ _expectedPlayers: val }),
  setSelectDirection: (val) => set({ selectDirection: val }),

  // Promise Setters
  setSelectedDirection: (direction) =>
    set((state) => {
      if (state._resolveDirectionPromise) {
        state._resolveDirectionPromise(direction);
      }
      return {
        selectedDirection: direction,
        _resolveDirectionPromise: null,
        selectDirection: false,
      };
    }),

  setSelectedCardsByPlayers: (payload) =>
    set((state) => {
      const updated = state.selectedCardsByPlayers.map((c) =>
        c.player_id === payload.player_id
          ? { ...c, ...payload } // duplicated
          : c
      );

      // add
      const exists = updated.some((c) => c.player_id === payload.player_id);
      if (!exists) updated.push(payload);

      // resolve promise
      if (
        updated.length === state._expectedPlayers &&
        state._resolveCardsPromise
      ) {
        state._resolveCardsPromise(updated);
      }

      return { selectedCardsByPlayers: updated };
    }),

  // Promise Section
  waitForAllCardsSelected: (totalPlayers) =>
    new Promise((resolve) => {
      set({
        _resolveCardsPromise: (selectedCards) => resolve(selectedCards),
        _expectedPlayers: totalPlayers,
      });
    }),

  waitForDirection: () =>
    new Promise((resolve) => {
      set({ _resolveDirectionPromise: resolve, selectDirection: true });
    }),
}));
