import { describe, it, expect, beforeEach } from "vitest";
import { useAnotherVictimStore } from "./AnotherVictimStore";

describe("useAnotherVictimStore", () => {
  beforeEach(() => {
    useAnotherVictimStore.setState({
      selectPlayerToStealSet: false,
      selectSetToStealOpen: false,
      targetPlayerToStealSet: null,
      targetSetToStealId: null,
      newStolenSet: null,
      _resolveTargetPromise: null,
      _resolveSetPromise: null,
    });
  });

  it("setselectPlayerToStealSet, setSelectSetToStealOpen y setNewStolenSet actualizan correctamente", () => {
    useAnotherVictimStore.getState().setselectPlayerToStealSet(true);
    expect(useAnotherVictimStore.getState().selectPlayerToStealSet).toBe(true);

    useAnotherVictimStore.getState().setSelectSetToStealOpen(true);
    expect(useAnotherVictimStore.getState().selectSetToStealOpen).toBe(true);

    useAnotherVictimStore.getState().setNewStolenSet({ id: 1 });
    expect(useAnotherVictimStore.getState().newStolenSet).toEqual({ id: 1 });
  });

  it("waitForTargetPlayerToStealSet y setTargetPlayerToStealSet funcionan correctamente", async () => {
    const promise = useAnotherVictimStore
      .getState()
      .waitForTargetPlayerToStealSet();

    expect(useAnotherVictimStore.getState()._resolveTargetPromise).toBeTypeOf(
      "function"
    );
    expect(useAnotherVictimStore.getState().selectPlayerToStealSet).toBe(true);

    useAnotherVictimStore.getState().setTargetPlayerToStealSet("Alice");

    const resolved = await promise;
    expect(resolved).toBe("Alice");

    const state = useAnotherVictimStore.getState();
    expect(state.targetPlayerToStealSet).toBe("Alice");
    expect(state.selectPlayerToStealSet).toBe(false);
    expect(state._resolveTargetPromise).toBeNull();
  });

  it("waitForTargetSetToStealId y setTargetSetToStealId funcionan correctamente", async () => {
    const promise = useAnotherVictimStore
      .getState()
      .waitForTargetSetToStealId();

    expect(useAnotherVictimStore.getState()._resolveSetPromise).toBeTypeOf(
      "function"
    );
    expect(useAnotherVictimStore.getState().selectSetToStealOpen).toBe(true);

    useAnotherVictimStore.getState().setTargetSetToStealId(42);

    const resolved = await promise;
    expect(resolved).toBe(42);

    const state = useAnotherVictimStore.getState();
    expect(state.targetSetToStealId).toBe(42);
    expect(state.selectSetToStealOpen).toBe(false);
    expect(state._resolveSetPromise).toBeNull();
  });
});
