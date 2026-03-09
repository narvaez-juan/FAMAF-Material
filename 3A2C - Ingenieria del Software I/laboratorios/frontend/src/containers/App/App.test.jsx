import { render, screen } from "@testing-library/react";
import App from "./App";

describe("App Container", () => {
  it("renders HomePage on root route", () => {
    render(<App />);
    expect(screen.getByText(/Death on the Cards/i)).toBeInTheDocument();
  });

  it("renders GameList on /games/list", () => {
    window.history.pushState({}, "", "/games/list");
    render(<App />);
    expect(screen.getByText(/list/i)).toBeInTheDocument();
  });

  it("renders GameRoom on /games/:gameId", () => {
    window.history.pushState({}, "", "/games/123");
    render(<App />);
    expect(screen.getByText(/Loading game/i)).toBeInTheDocument();
  });

  it("renders Lobby on /games/:gameId/lobbies", () => {
    window.history.pushState({}, "", "/games/123/lobbies");
    render(<App />);
    expect(screen.getByText(/Lobby/i)).toBeInTheDocument();
  });

  it("renders JoinGame on /games/:gameId/join", () => {
    window.history.pushState({}, "", "/games/123/join");
    render(<App />);
    expect(screen.getByText(/Join Existing Game/i)).toBeInTheDocument();
  });
});
