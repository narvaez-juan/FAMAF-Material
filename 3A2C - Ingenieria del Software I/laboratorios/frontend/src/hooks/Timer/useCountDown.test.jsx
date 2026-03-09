import { beforeEach, afterEach, vi, expect } from "vitest";
import { render, act } from "@testing-library/react";
import useCountDown from "./useCountDown";

/**
 * Renderiza un componente de test que usa el hook y expone result.current
 * @param {string} key
 * @param {number} defaultSeconds
 * @returns {{ result: { current: any }, rerender: Function, unmount: Function }}
 */
function renderUseCountDown(key, defaultSeconds = 60) {
  const result = { current: null };

  function TestComponent({ k, sec }) {
    result.current = useCountDown(k, sec);
    return null;
  }

  const utils = render(<TestComponent k={key} sec={defaultSeconds} />);
  return { ...utils, result };
}

/**
 * Avanza segundos usando fake timers
 * @param {number} seconds
 */
function advanceSec(seconds = 1) {
  act(() => {
    vi.advanceTimersByTime(seconds * 1000);
  });
}

/* localStorage helpers */
function setLocalStorage(key, value) {
  window.localStorage.setItem(key, String(value));
}
function clearLocalStorage() {
  window.localStorage.clear();
}

function getLocalStorage(key) {
  return window.localStorage.getItem(key);
}

beforeEach(() => {
  vi.clearAllMocks();
  clearLocalStorage();
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

describe("useCountDown — unit", () => {
  it("inicializa con el valor pasado", () => {
    const { result, unmount } = renderUseCountDown("timer_test_key", 60);
    expect(result.current.secondsLeft).toBe(60);
    unmount();
  });

  it("decrementa 1 por segundo cuando se pasa el valor inicial", () => {
    const { result, unmount } = renderUseCountDown("timer_test_key", 3);
    expect(result.current.secondsLeft).toBe(3);

    act(() => {
      result.current.start();
    });
    advanceSec(1);
    expect(result.current.secondsLeft).toBe(2);
    unmount();
  });

  it("resetea el valor correctamente al inicial", () => {
    const { result, unmount } = renderUseCountDown("timer_test_key", 60);
    expect(result.current.secondsLeft).toBe(60);

    act(() => {
      result.current.start();
    });
    advanceSec(1);
    expect(result.current.secondsLeft).toBe(59);

    act(() => {
      result.current.reset();
    });

    expect(result.current.secondsLeft).toBe(60);

    unmount();
  });

  it("al hacer stop el timer no avanza", () => {
    const { result, unmount } = renderUseCountDown("timer_test_key", 60);
    expect(result.current.secondsLeft).toBe(60);

    act(() => {
      result.current.start();
    });
    advanceSec(1);
    expect(result.current.secondsLeft).toBe(59);

    act(() => {
      result.current.stop();
    });

    expect(result.current.secondsLeft).toBe(59);
    unmount();
  });
});

// 3) persistencia (localStorage)
describe("useCountDown — persistence", () => {
  it("inicializa desde localStorage si existe", () => {
    setLocalStorage("timer_test_key", 50);

    const { result, unmount } = renderUseCountDown("timer_test_key", 60);
    expect(result.current.secondsLeft).toBe(50);
    unmount();
  });

  it("escribe en localStorage cuando cambia secondsLeft", () => {
    const { result, unmount } = renderUseCountDown("timer_test_key", 3);
    expect(result.current.secondsLeft).toBe(3);

    act(() => {
      result.current.start();
    });
    advanceSec(1);

    expect(getLocalStorage("timer_test_key")).toBe("2");

    unmount();
  });

  it("resetea el localStorage al valor inicial", () => {
    const { result, unmount } = renderUseCountDown("timer_test_key", 3);
    expect(result.current.secondsLeft).toBe(3);

    act(() => {
      result.current.start();
    });

    advanceSec(1);

    expect(result.current.secondsLeft).toBe(2);

    act(() => {
      result.current.reset();
    });

    expect(getLocalStorage("timer_test_key")).toBe("3");

    unmount();
  });
});

// 4) múltiples instancias
describe("useCountDown — robustness", () => {
  it("dos instancias independientes", () => {
    // Instancia 1
    const { result: result1, unmount: unmount1 } = renderUseCountDown(
      "timer_test_key1",
      20
    );
    expect(result1.current.secondsLeft).toBe(20);

    // Instancia 2
    const { result: result2, unmount: unmount2 } = renderUseCountDown(
      "timer_test_key2",
      10
    );
    expect(result2.current.secondsLeft).toBe(10);

    act(() => {
      result1.current.start();
    });
    act(() => {
      result2.current.start();
    });
    advanceSec(1);

    expect(result1.current.secondsLeft).toBe(19);
    expect(result2.current.secondsLeft).toBe(9);
    unmount1();
    unmount2();
  });
});
