import PlayerForm from "./JoinGameForm";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";

describe("PlayerForm", () => {
  let mockOnSubmit;

  beforeEach(() => {
    vi.clearAllMocks();
    mockOnSubmit = vi.fn();
  });

  describe("Default state", () => {
    it("renders all form fields, submit and reset button", () => {
      render(<PlayerForm onSubmit={mockOnSubmit} />);

      expect(screen.getByLabelText(/Player name/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Player birth date/i)).toBeInTheDocument();

      const submitBtn = screen.getByRole("button", { name: /Submit/i });
      const resetBtn = screen.getByRole("button", {
        name: /Autocompletar|Autocomplete|Reset/i,
      });
      expect(submitBtn).toBeInTheDocument();
      expect(resetBtn).toBeInTheDocument();
      expect(submitBtn).not.toBeDisabled();
    });
  });

  describe("Submit flow", () => {
    it("calls onSubmit with valid form values", async () => {
      mockOnSubmit = vi.fn().mockResolvedValueOnce();
      render(<PlayerForm onSubmit={mockOnSubmit} />);

      await userEvent.type(screen.getByLabelText(/Player name/i), "Alice");
      await userEvent.type(
        screen.getByLabelText(/Player birth date/i),
        "2000-01-01"
      );

      await userEvent.click(screen.getByRole("button", { name: /Submit/i }));

      await waitFor(() => {
        expect(mockOnSubmit).toHaveBeenCalledWith(
          {
            player_name: "Alice",
            player_birth_date: "2000-01-01",
          },
          undefined // gameId es undefined en este test
        );
      });
    });
  });

  describe("Reset button", () => {
    it("autocompletes form fields when reset button is clicked", async () => {
      render(<PlayerForm onSubmit={mockOnSubmit} />);

      const nameInput = screen.getByLabelText(/Player name/i);
      const birthDateInput = screen.getByLabelText(/Player birth date/i);

      expect(nameInput).toHaveValue("");
      expect(birthDateInput).toHaveValue("");

      await userEvent.click(
        screen.getByRole("button", {
          name: /Autocompletar|Autocomplete|Reset/i,
        })
      );

      await waitFor(() => {
        expect(nameInput).not.toHaveValue("");
        expect(birthDateInput).not.toHaveValue("");
        expect(/^\d{4}-\d{2}-\d{2}$/.test(birthDateInput.value)).toBe(true);
      });
    });
  });

  describe("Validation behavior", () => {
    it("shows validation errors and does not call onSubmit when required fields are empty", async () => {
      render(<PlayerForm onSubmit={mockOnSubmit} />);

      const submitBtn = screen.getByRole("button", { name: /Submit/i });
      await userEvent.click(submitBtn);

      const nameInput = screen.getByLabelText(/Player name/i);
      const birthDateInput = screen.getByLabelText(/Player birth date/i);

      expect(nameInput).toBeInvalid();
      expect(birthDateInput).toBeInvalid();

      expect(mockOnSubmit).not.toHaveBeenCalled();
    });

    it("disables submit and shows creating state while onSubmit promise is pending", async () => {
      let resolvePromise;
      const pending = new Promise((res) => {
        resolvePromise = res;
      });
      mockOnSubmit = vi.fn(() => pending);

      render(<PlayerForm onSubmit={mockOnSubmit} />);

      await userEvent.type(screen.getByLabelText(/Player name/i), "Bob");
      await userEvent.type(
        screen.getByLabelText(/Player birth date/i),
        "1990-01-01"
      );

      const submitBtn = screen.getByRole("button", { name: /Submit/i });
      await userEvent.click(submitBtn);

      expect(submitBtn).toBeDisabled();
      expect(submitBtn).toHaveTextContent(/Submitting.../i);

      resolvePromise();
      await waitFor(() => expect(mockOnSubmit).toHaveBeenCalled());
    });

    it("does not call onSubmit when client-side validation fails", async () => {
      render(<PlayerForm onSubmit={mockOnSubmit} />);

      await userEvent.click(screen.getByRole("button", { name: /Submit/i }));

      expect(mockOnSubmit).not.toHaveBeenCalled();
    });
  });
});
