// test/WSServices.test.js
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";

vi.mock("socket.io-client", () => {
  return {
    io: vi.fn(() => {
      const mockSocket = {
        on: vi.fn((event, cb) => {
          if (event === "connect") {
            setTimeout(() => {
              try {
                cb(); 
              } catch (e) {
                console.error("Mock connect error:", e);
              }
            }, 0);
          }
        }),
        emit: vi.fn(),
        disconnect: vi.fn(),
        id: "mock-socket-id",
      };
      return mockSocket;
    }),
  };
});

describe("WSServices", () => {
  beforeEach(() => {
    vi.resetModules();
    vi.clearAllMocks();

    global.localStorage = {
      store: {},
      getItem: vi.fn(function (key) {
        return this.store[key] || null;
      }),
      setItem: vi.fn(function (key, value) {
        this.store[key] = String(value);
      }),
      removeItem: vi.fn(function (key) {
        delete this.store[key];
      }),
      clear: vi.fn(function () {
        this.store = {};
      }),
    };
  });

  afterEach(() => {
    vi.restoreAllMocks();
    delete global.localStorage;
  });

  it("should create and cache socket instance", async () => {
    const { io } = await import("socket.io-client");
    const { default: getSocket } = await import("../services/WSServices");

    const socket1 = await getSocket();

    expect(io).toHaveBeenCalledTimes(1);
    expect(io).toHaveBeenCalledWith("http://localhost:8000", expect.any(Object));
    expect(socket1.id).toBe("mock-socket-id");

    io.mockClear();
    const socket2 = await getSocket();

    expect(io).not.toHaveBeenCalled();
    expect(socket2).toBe(socket1);
  });

  it("should support .on and .emit on the returned socket", async () => {
    const { default: getSocket } = await import("../services/WSServices");

    const socket = await getSocket();

    const handler = vi.fn();

    socket.on("my-event", handler);
    expect(socket.on).toHaveBeenCalledWith("my-event", handler);

    socket.emit("my-event", "data1", 42);
    expect(socket.emit).toHaveBeenCalledWith("my-event", "data1", 42);
  });
});
