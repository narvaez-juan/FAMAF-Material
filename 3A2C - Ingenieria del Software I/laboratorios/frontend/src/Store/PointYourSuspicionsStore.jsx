import { create } from "zustand";

export const usePointYourSuspicionsStore = create((set) => ({
  playerId: null,
  selectPlayerSuspicions: false,
  selectedPlayers: [],
  _expectedPlayers: 0,
  selectPlayerInfo: null,

  // Normal setters
  setSelectPlayerSuspicions: (val) => set({ selectPlayerSuspicions: val }),
  setExpectedPlayers: (val) => set({ _expectedPlayers: val }),
  setSelectPlayerInfo: (val) => set({ selectPlayerInfo: val }),
  setPlayerId: (val) => set({ playerId: val }),
  clearSelectedPlayers: () => set({ selectedPlayers: [] }),

  // Promise Setters
  setSelectedPlayers: (payload) =>
    set((state) => {
      const updated = state.selectedPlayers.map((c) =>
        c.player_id === payload.player_id &&
        c.target_player_id === payload.target_player_id
          ? { ...c, ...payload }
          : c
      );

      // add if not exists
      const exists = updated.some(
        (c) =>
          c.player_id === payload.player_id &&
          c.target_player_id === payload.target_player_id
      );
      if (!exists) updated.push(payload);

      if (
        updated.length === state._expectedPlayers &&
        state._resolvePlayersPromise
      ) {
        state._resolvePlayersPromise(updated);
      }

      return { selectedPlayers: updated };
    }),

  // Setters

  // Promise Section
  waitForAllPlayersSelected: (totalPlayers) =>
    new Promise((resolve) => {
      set({
        _resolvePlayersPromise: (selectedPlayers) => resolve(selectedPlayers),
        _expectedPlayers: totalPlayers,
      });
    }),
}));
