import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { vi } from "vitest";
import SelectPlayerToStealSetModal from "./SelectPlayerForSets";

describe("SelectPlayerToStealSetModal", () => {
  const players = [
    { id_jugador: 1, nombre: "jere" },
    { id_jugador: 2, nombre: "fran" },
    { id_jugador: 3, nombre: "nax" },
  ];

  test("shows message when there are no other players to steal from", () => {
    render(
      <SelectPlayerToStealSetModal
        players={[{ id_jugador: 1, nombre: "jere" }]}
        playerId={1}
      />
    );

    expect(
      screen.getByText(/There are no other players to steal from/i)
    ).toBeInTheDocument();
    const confirm = screen.getByRole("button", { name: /Confirm Steal/i });
    expect(confirm).toBeDisabled();
  });

  test("renders list excluding current player and allows selection + confirm", () => {
    const onConfirm = vi.fn();
    render(
      <SelectPlayerToStealSetModal
        players={players}
        playerId={1}
        onConfirm={onConfirm}
      />
    );

    expect(screen.queryByText("jere")).not.toBeInTheDocument();

    expect(screen.getByText("fran")).toBeInTheDocument();
    expect(screen.getByText("nax")).toBeInTheDocument();

    const confirm = screen.getByRole("button", { name: /Confirm Steal/i });
    expect(confirm).toBeDisabled();

    fireEvent.click(screen.getByText("fran"));
    expect(confirm).not.toBeDisabled();

    fireEvent.click(confirm);
    expect(onConfirm).toHaveBeenCalledWith(
      expect.objectContaining({ id_jugador: 2, nombre: "fran" })
    );
  });

  test("cancel button calls onCancel if provided", () => {
    const onCancel = vi.fn();
    render(
      <SelectPlayerToStealSetModal
        players={players}
        playerId={1}
        onCancel={onCancel}
      />
    );

    const cancel = screen.getByRole("button", { name: /Cancel/i });
    fireEvent.click(cancel);
    expect(onCancel).toHaveBeenCalled();
  });
});
