// src/pages/GameList.test.jsx
import { describe, test, expect, vi, beforeEach } from "vitest";
import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";

/**
 * IMPORTANTE:
 * - vi.mock() se declara ANTES de importar los módulos reales que queremos mockear,
 *   por eso las mocks están arriba y las importaciones reales abajo.
 */

// mock para useNavigate
const navigateMock = vi.fn();

// Mock del módulo de socket (default export)
vi.mock("../services/WSServices", () => ({
  default: vi.fn(),
}));

// Mock del componente GameCard (default export). Devuelve un componente simple
vi.mock("../components/GameCard/GameCard", () => ({
  default: (props) => (
    <div data-testid={`game-card-${props.gameName}`}>
      <span>{props.gameName}</span>
      <div>
        {props.currentPlayers}/{props.maxPlayers}
      </div>
      <button data-testid={`join-${props.gameName}`} onClick={props.onJoin}>
        Join
      </button>
    </div>
  ),
}));

// Mock de react-router-dom (useNavigate y useParams)
vi.mock("react-router-dom", () => ({
  useNavigate: () => navigateMock,
  useParams: () => ({ gameId: "123" }),
}));

// Ahora importamos los "reales" (mockeados por vitest)
import getSocket from "../services/WSServices";
import GameList from "./GameList";

describe("GameList component (Vitest)", () => {
  let mockSocket;

  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();

    mockSocket = {
      emit: vi.fn(),
      on: vi.fn(),
      off: vi.fn(),
    };

    // getSocket es el default mock (vi.fn()), lo configuramos para que resuelva con mockSocket
    getSocket.mockResolvedValue(mockSocket);
  });

  test("muestra mensaje cuando no hay partidas", async () => {
    render(<GameList />);

    // Esperamos a que el componente registre el handler 'game_list'
    await waitFor(() =>
      expect(mockSocket.on).toHaveBeenCalledWith(
        "game_list",
        expect.any(Function)
      )
    );

    // Extraemos el handler registrado para 'game_list' y lo invocamos con lista vacía
    const handler = mockSocket.on.mock.calls.find(
      (c) => c[0] === "game_list"
    )[1];
    handler([]);

    // Debe aparecer el mensaje por defecto (case-insensitive)
    expect(
      await screen.findByText(/No games available at the moment/i)
    ).toBeInTheDocument();
  });

  test("renderiza GameCard cuando recibe una lista de partidas", async () => {
    render(<GameList />);

    await waitFor(() =>
      expect(mockSocket.on).toHaveBeenCalledWith(
        "game_list",
        expect.any(Function)
      )
    );

    const handler = mockSocket.on.mock.calls.find(
      (c) => c[0] === "game_list"
    )[1];

    const games = [
      { id: "g1", name: "Sala 1", currentPlayers: 1, maxPlayers: 4 },
      { id: "g2", name: "Sala 2", currentPlayers: 2, maxPlayers: 4 },
    ];

    // Simulamos la llegada de la lista desde el servidor
    handler(games);

    // Cada GameCard (mock) debe renderizarse
    expect(await screen.findByTestId("game-card-Sala 1")).toBeInTheDocument();
    expect(await screen.findByTestId("game-card-Sala 2")).toBeInTheDocument();
  });

  test("guarda RoomID desde useParams y navega al hacer join", async () => {
    render(<GameList />);

    // Como useParams() devuelve { gameId: "123" } en el mock, el effect debería guardar RoomID
    await waitFor(() => expect(localStorage.getItem("RoomID")).toBe("123"));

    // Registrado el handler, lo usamos para inyectar partidas
    const handler = mockSocket.on.mock.calls.find(
      (c) => c[0] === "game_list"
    )[1];
    const games = [
      { id: "g1", name: "Sala 1", currentPlayers: 1, maxPlayers: 4 },
    ];
    handler(games);

    // Hacemos click en el botón Join del GameCard mockeado
    const joinBtn = await screen.findByTestId("join-Sala 1");
    fireEvent.click(joinBtn);

    // Debe haberse llamado navigate con la ruta esperada
    expect(navigateMock).toHaveBeenCalledWith("/games/g1/join/");
  });
});
