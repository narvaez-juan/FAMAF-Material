import { create } from "zustand";

export const useEventCardStore = create((set) => ({
  playerHasPlayedEvent: false,

  eventCardClicked: null,
  selectPlayer: false,
  targetPlayer: null,

  // Secret revealing
  votedToReveal: false,
  votedPlayerId: null,
  secretsByPlayer: {},

  // Normal Setters
  setSelectPlayer: (val) => set({ selectPlayer: val }),
  setEventCardClicked: (card) => set({ eventCardClicked: card }),
  clearEventCardClicked: () => set({ eventCardClicked: null }),
  setPlayerHasPlayedEvent: (val) => set({ playerHasPlayedEvent: val }),

  // Normal Setters - Secret Revealing
  setVotedToReveal: (val) => set({ votedToReveal: val }),
  setVotedPlayerId: (val) => set({ votedPlayerId: val }),

  setSecrets: (playerId, secrets) =>
    set((state) => ({
      secretsByPlayer: {
        ...state.secretsByPlayer,
        [playerId]: secrets,
      },
    })),

  // Promise Setters
  setTargetPlayer: (player) =>
    set((state) => {
      if (state._resolveTargetPromise) {
        state._resolveTargetPromise(player);
      }
      return {
        targetPlayer: player,
        selectPlayer: false,
        _resolveTargetPromise: null,
      };
    }),

  // Promise Section
  waitForTargetPlayer: () =>
    new Promise((resolve) => {
      set({ _resolveTargetPromise: resolve, selectPlayer: true });
    }),
}));
