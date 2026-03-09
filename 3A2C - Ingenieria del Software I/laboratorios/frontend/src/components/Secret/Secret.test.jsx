import { describe, it, expect } from "vitest";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import Secret from "./Secret";

describe("Secret component", () => {
  it(
    ("renders correctly the card",
    () => {
      render(<Secret image="03-secret_murderer.png" alt="murderer" />);
      const img = screen.getByAltText("murderer");
      expect(img).toBeInTheDocument();
      expect(img).toHaveAttribute("src", "03-secret_murderer.png");
      expect(img).toHaveAttribute("draggable", "false");
    })
  );

  it(
    ("use alt by default if not given a prop",
    () => {
      render(<Secret image="03-secret_murderer.png" />);
      const img = screen.getByAltText("Secret");
      expect(img).toBeInTheDocument();
    })
  );

  it("shows the card back when isRevealed is false", () => {
    render(<Secret image="03-secret_murderer.png" isRevealed={false} />);
    const img = screen.getByAltText("Secret");
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute("src", "/Cartas/05-secret_front.png");
  });
});
