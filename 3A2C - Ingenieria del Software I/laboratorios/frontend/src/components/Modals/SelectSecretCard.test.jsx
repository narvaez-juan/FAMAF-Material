import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { vi } from "vitest";
import SelectSecretCardModal from "./SelectSecretCard";

const makeSecret = (id, image = "a.png", isRevealed = false) => ({
  id,
  image,
  isRevealed,
});

describe("SelectSecretCardModal", () => {
  test("renders correct header for REVEAL effect", () => {
    render(
      <SelectSecretCardModal
        effect="REVEAL"
        secrets={[]}
        isOwner={false}
        onConfirm={() => {}}
      />
    );
    expect(screen.getByText(/Choose a secret to reveal/i)).toBeInTheDocument();
  });

  test("renders correct header for HIDE effect", () => {
    render(
      <SelectSecretCardModal
        effect="HIDE"
        secrets={[]}
        isOwner={false}
        onConfirm={() => {}}
      />
    );
    expect(screen.getByText(/Choose a secret to hide/i)).toBeInTheDocument();
  });

  test("renders correct header for STEAL effect", () => {
    render(
      <SelectSecretCardModal
        effect="STEAL"
        secrets={[]}
        isOwner={false}
        onConfirm={() => {}}
      />
    );
    expect(screen.getByText(/Choose a secret to steal/i)).toBeInTheDocument();
  });

  test("shows no secrets message when secrets empty", () => {
    render(
      <SelectSecretCardModal
        effect="REVEAL"
        secrets={[]}
        isOwner={false}
        onConfirm={() => {}}
      />
    );
    expect(screen.getByText(/No secrets available/i)).toBeInTheDocument();
  });

  test("selecting a secret enables confirm and calls onConfirm with selected id", () => {
    const secrets = [
      makeSecret(1, "a.png", false),
      makeSecret(2, "b.png", true),
    ];
    const onConfirm = vi.fn();
    render(
      <SelectSecretCardModal
        effect="STEAL"
        secrets={secrets}
        isOwner={false}
        onConfirm={onConfirm}
      />
    );

    const secretElements = screen.getAllByRole("img");
    expect(secretElements.length).toBeGreaterThan(0);
    fireEvent.click(secretElements[0]);

    const confirm = screen.getByRole("button", { name: /Steal|Reveal|Hide/i });
    expect(confirm).not.toBeDisabled();

    fireEvent.click(confirm);
    expect(onConfirm).toHaveBeenCalledWith(1);
  });
});
