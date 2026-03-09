import { describe, it, expect, vi, beforeEach, window } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";
import GameForm from "./GameForm";

describe("GameForm", () => {
  let mockOnSubmit;

  beforeEach(() => {
    vi.clearAllMocks();
    mockOnSubmit = vi.fn();
  });

  describe("Default state", () => {
    it("renders all form fields, submit and Autocomplete button", () => {
      render(<GameForm onSubmit={mockOnSubmit} />);

      expect(screen.getByLabelText(/Game name/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Min players/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Max players/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Player name/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Player birth date/i)).toBeInTheDocument();

      const submitBtn = screen.getByRole("button", { name: /Create/i });
      const AutocompleteBtn = screen.getByRole("button", {
        name: /Autocomplete/i,
      });
      expect(submitBtn).toBeInTheDocument();
      expect(AutocompleteBtn).toBeInTheDocument();
      expect(submitBtn).not.toBeDisabled();
    });
  });
  describe("Autocomplete button", () => {
    it("fills all form fields with data when clicked and clears errors", async () => {
      render(<GameForm onSubmit={mockOnSubmit} />);

      await userEvent.click(screen.getByRole("button", { name: /Create/i }));
      expect(
        await screen.findByText(/Game name is required/i)
      ).toBeInTheDocument();

      await userEvent.click(
        screen.getByRole("button", { name: /Autocomplete/i })
      );

      const gameNameInput = screen.getByLabelText(/Game name/i);
      const playerNameInput = screen.getByLabelText(/Player name/i);
      const minPlayersInput = screen.getByLabelText(/Min players/i);
      const maxPlayersInput = screen.getByLabelText(/Max players/i);
      const birthDateInput = screen.getByLabelText(/Player birth date/i);

      expect(gameNameInput.value).toBeTruthy();
      expect(playerNameInput.value).toBeTruthy();
      expect(birthDateInput.value).toBeTruthy();

      expect(minPlayersInput).toHaveValue(2);
      expect(maxPlayersInput).toHaveValue(6);

      expect(
        screen.queryByText(/Game name is required/i)
      ).not.toBeInTheDocument();
    });
  });
  describe("Submit flow", () => {
    it("calls onSubmit with valid form values", async () => {
      mockOnSubmit = vi.fn().mockResolvedValueOnce();
      render(<GameForm onSubmit={mockOnSubmit} />);

      await userEvent.type(
        screen.getByLabelText(/Game name/i),
        "Mystery Mansion"
      );
      await userEvent.type(screen.getByLabelText(/Min players/i), "2");
      await userEvent.type(screen.getByLabelText(/Max players/i), "4");
      await userEvent.type(screen.getByLabelText(/Player name/i), "Alice");
      await userEvent.type(
        screen.getByLabelText(/Player birth date/i),
        "2000-01-01"
      );

      await userEvent.click(screen.getByRole("button", { name: /Create/i }));

      await waitFor(() => {
        expect(mockOnSubmit).toHaveBeenCalledWith({
          game_name: "Mystery Mansion",
          min_players: "2",
          max_players: "4",
          player_name: "Alice",
          player_birth_date: "2000-01-01",
        });
      });
    });
  });

  describe("Validation behavior", () => {
    it("shows validation errors and does not call onSubmit when required fields are empty", async () => {
      render(<GameForm onSubmit={mockOnSubmit} />);

      const submitBtn = screen.getByRole("button", { name: /Create/i });
      await userEvent.click(submitBtn);

      expect(
        await screen.findByText(/Game name is required/i)
      ).toBeInTheDocument();
      expect(
        await screen.findByText(/Minimum number of players is required/i)
      ).toBeInTheDocument();
      expect(
        await screen.findByText(/Maximum number of players is required/i)
      ).toBeInTheDocument();
      expect(
        await screen.findByText(/Player name is required/i)
      ).toBeInTheDocument();
      expect(
        await screen.findByText(/Player birth date is required/i)
      ).toBeInTheDocument();

      expect(mockOnSubmit).not.toHaveBeenCalled();
    });

    it("prevents submit when min_players > max_players and shows range error", async () => {
      render(<GameForm onSubmit={mockOnSubmit} />);

      await userEvent.type(screen.getByLabelText(/Game name/i), "Test Game");
      await userEvent.type(screen.getByLabelText(/Min players/i), "5");
      await userEvent.type(screen.getByLabelText(/Max players/i), "2");
      await userEvent.click(screen.getByRole("button", { name: /Create/i }));

      expect(
        await screen.findByText(
          /Minimum number of players must be less than maximum number of players/i
        )
      ).toBeInTheDocument();
      expect(mockOnSubmit).not.toHaveBeenCalled();
    });

    it("prevents submit when min_players < 2 and max_players > 6 and shows error", async () => {
      render(<GameForm onSubmit={mockOnSubmit} />);

      await userEvent.type(screen.getByLabelText(/Game name/i), "Test Game");
      await userEvent.type(screen.getByLabelText(/Min players/i), "1");
      await userEvent.type(screen.getByLabelText(/Max players/i), "7");
      await userEvent.click(screen.getByRole("button", { name: /Create/i }));

      expect(
        await screen.findByText(
          /Minimum number of players must be between 2 and 6/i
        )
      ).toBeInTheDocument();
      expect(
        await screen.findByText(
          /Maximum number of players must be between 2 and 6/i
        )
      ).toBeInTheDocument();

      expect(mockOnSubmit).not.toHaveBeenCalled();
    });

    it("disables submit and shows creating state while onSubmit promise is pending", async () => {
      // create promise
      let resolvePromise;
      const pending = new Promise((res) => {
        resolvePromise = res;
      });
      mockOnSubmit = vi.fn(() => pending);

      render(<GameForm onSubmit={mockOnSubmit} />);

      await userEvent.type(screen.getByLabelText(/Game name/i), "Game");
      await userEvent.type(screen.getByLabelText(/Min players/i), "2");
      await userEvent.type(screen.getByLabelText(/Max players/i), "4");
      await userEvent.type(screen.getByLabelText(/Player name/i), "Bob");
      await userEvent.type(
        screen.getByLabelText(/Player birth date/i),
        "1990-01-01"
      );

      const submitBtn = screen.getByRole("button", { name: /Create/i });
      await userEvent.click(submitBtn);

      // while promise is pending, create button should be "Creating..."
      expect(submitBtn).toBeDisabled();
      expect(submitBtn).toHaveTextContent(/Creating.../i);

      // do promise to clean
      resolvePromise();
      await waitFor(() => expect(mockOnSubmit).toHaveBeenCalled());
    });

    it("does not call onSubmit when client-side validation fails", async () => {
      render(<GameForm onSubmit={mockOnSubmit} />);

      await userEvent.type(screen.getByLabelText(/Game name/i), "G");
      // dejar min/max vacíos intencionalmente
      await userEvent.click(screen.getByRole("button", { name: /Create/i }));

      expect(mockOnSubmit).not.toHaveBeenCalled();
      expect(
        await screen.findByText(/Minimum number of players is required/i)
      ).toBeInTheDocument();
    });
  });
});
