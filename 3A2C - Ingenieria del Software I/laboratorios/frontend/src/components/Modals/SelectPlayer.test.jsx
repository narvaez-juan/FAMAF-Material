import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { vi } from "vitest";
import SelectPlayerModal from "./SelectPlayer";

describe("SelectPlayerModal", () => {
  const players = [
    { id_jugador: 1, nombre: "Jere" },
    { id_jugador: 2, nombre: "fran" },
    { id_jugador: 3, nombre: "max" },
  ];

  test("renders list of players and disabled confirm initially", () => {
    const onConfirm = vi.fn();
    render(
      <SelectPlayerModal
        players={players}
        playerId={1}
        effect="Steal"
        onConfirm={onConfirm}
      />
    );

    expect(screen.getByText("Jere")).toBeInTheDocument();
    expect(screen.getByText("fran")).toBeInTheDocument();
    expect(screen.getByText("max")).toBeInTheDocument();

    const confirm = screen.getByRole("button", { name: /select/i });
    expect(confirm).toBeDisabled();
  });

  test("selecting a valid player enables confirm and calls onConfirm with correct payload", () => {
    const onConfirm = vi.fn();
    render(
      <SelectPlayerModal
        players={players}
        playerId={1}
        effect="Steal"
        onConfirm={onConfirm}
      />
    );

    const franButton = screen.getByText("fran");
    fireEvent.click(franButton);

    const confirm = screen.getByRole("button", { name: /select/i });
    expect(confirm).not.toBeDisabled();

    fireEvent.click(confirm);
    expect(onConfirm).toHaveBeenCalledWith({ id: 2, name: "fran" });
  });

  test("cannot select self when effect prohibits it (Reveal by Target example)", () => {
    const onConfirm = vi.fn();
    render(
      <SelectPlayerModal
        players={players}
        playerId={2}
        effect="Reveal by Target"
        onConfirm={onConfirm}
      />
    );

    const franButton = screen.getByText("fran");
    fireEvent.click(franButton);

    const confirm = screen.getByRole("button", { name: /select/i });
    expect(confirm).toBeDisabled();
  });
});
