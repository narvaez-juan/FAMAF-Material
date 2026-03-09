import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { vi } from "vitest";
import CreateGame from "./CreateGame";
import { MemoryRouter } from "react-router-dom";

// Mock HTTPServices
const mockCreateGame = vi.fn();
vi.mock("../services/HTTPServices", () => ({
  createHttpService: () => ({
    createGame: mockCreateGame,
  }),
}));

// Mock getSocket
const mockEmit = vi.fn();
const mockSocket = { emit: mockEmit };
vi.mock("../services/WSServices", () => ({
  default: vi.fn(() => Promise.resolve(mockSocket)),
}));

// Mock useNavigate
const mockNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe("CreateGame page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it("renders form and submits to create a game", async () => {
    render(
      <MemoryRouter>
        <CreateGame />
      </MemoryRouter>
    );

    // Fill form fields
    fireEvent.change(screen.getByPlaceholderText(/Your name/i), {
      target: { value: "Test Player" },
    });
    fireEvent.change(screen.getByLabelText(/Game name/i), {
      target: { value: "Test Game" },
    });
    fireEvent.change(screen.getByLabelText(/Min players/i), {
      target: { value: "2" },
    });
    fireEvent.change(screen.getByLabelText(/Max players/i), {
      target: { value: "4" },
    });
    fireEvent.change(screen.getByLabelText(/Player birth date/i), {
      target: { value: "2000-01-01" },
    });

    // Mock server response
    mockCreateGame.mockResolvedValue({
      game_id: "42",
      player_id: "abc123",
    });

    // Submit form (busca el botón por su texto real)
    fireEvent.click(screen.getByText(/Create$/i));

    await waitFor(() => {
      expect(mockCreateGame).toHaveBeenCalled();
      expect(localStorage.getItem("RoomID")).toBe("42");
      expect(mockEmit).toHaveBeenCalledWith("join_game", "game:42");
      expect(mockNavigate).toHaveBeenCalledWith("/games/42/lobbies", {
        state: { playerId: "abc123" },
      });
    });
  });

  it("shows error if game name is already in use", async () => {
    render(
      <MemoryRouter>
        <CreateGame />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/Game name/i), {
      target: { value: "Test Game" },
    });
    fireEvent.change(screen.getByPlaceholderText(/Your name/i), {
      target: { value: "Test Player" },
    });
    fireEvent.change(screen.getByLabelText(/Min players/i), {
      target: { value: "2" },
    });
    fireEvent.change(screen.getByLabelText(/Max players/i), {
      target: { value: "4" },
    });
    fireEvent.change(screen.getByLabelText(/Player birth date/i), {
      target: { value: "2000-01-01" },
    });

    mockCreateGame.mockRejectedValue({ status: 409 });

    fireEvent.click(screen.getByText(/Create$/i));

    await waitFor(() => {
      expect(screen.getByText(/Game name already in use/i)).toBeInTheDocument();
    });
  });
});
