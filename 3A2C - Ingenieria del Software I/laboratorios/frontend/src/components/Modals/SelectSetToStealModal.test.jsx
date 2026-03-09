import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { vi } from "vitest";
import SelectSetToStealModal from "./SelectSetToStealModal";

describe("SelectSetToStealModal", () => {
  test("shows loading state when loading=true", () => {
    render(
      <SelectSetToStealModal loading={true} sets={[]} playerName="fran" />
    );
    expect(screen.getByText(/Loading sets.../i)).toBeInTheDocument();
  });

  test("shows message when player doesn't have sets", () => {
    render(
      <SelectSetToStealModal loading={false} sets={[]} playerName="fran" />
    );
    expect(
      screen.getByText(/This player doesn't have any sets to steal/i)
    ).toBeInTheDocument();
  });

  test("renders sets and clicking a set calls onConfirm with set id", () => {
    const onConfirm = vi.fn();
    const sets = [
      { set_play_id: 10, card_game_images: ["a.png"], card_game_ids: [1] },
      {
        set_play_id: 11,
        card_game_images: ["b.png", "c.png"],
        card_game_ids: [2, 3],
      },
    ];

    render(
      <SelectSetToStealModal
        loading={false}
        sets={sets}
        playerName="fran"
        onConfirm={onConfirm}
      />
    );

    expect(screen.getByText(/1 Cards/i)).toBeInTheDocument();
    expect(screen.getByText(/2 Cards/i)).toBeInTheDocument();

    const buttons = screen.getAllByRole("button", { name: /STEAL/i });
    const setButtons = screen.getAllByRole("button");
    const target = setButtons.find(
      (b) => b.textContent && b.textContent.includes("STEAL")
    );
    expect(target).toBeTruthy();
    fireEvent.click(target);

    expect(onConfirm).toHaveBeenCalledWith(10);
  });

  test("cancel button calls onCancel", () => {
    const onCancel = vi.fn();
    render(
      <SelectSetToStealModal
        loading={false}
        sets={[]}
        playerName="fran"
        onCancel={onCancel}
      />
    );
    const cancel = screen.getByRole("button", { name: /Cancel/i });
    fireEvent.click(cancel);
    expect(onCancel).toHaveBeenCalled();
  });
});
