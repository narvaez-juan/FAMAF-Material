import { describe, it, expect, vi } from "vitest";
import "@testing-library/jest-dom";
import { render, screen, fireEvent } from "@testing-library/react";
import Card from "./Card";

describe("Card component", () => {
  it("renderiza la imagen correctamente", () => {
    render(<Card image="00-help.png" alt="ayuda" />);
    const img = screen.getByAltText("ayuda");
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute("src", "/Cartas/00-help.png");
    expect(img).toHaveAttribute("draggable", "false");
  });

  it("usa el alt por defecto si no se pasa prop", () => {
    render(<Card image="/Cartas/00-help.png" />);
    const img = screen.getByAltText("card");
    expect(img).toBeInTheDocument();
  });

  it("renders placeholder when showPlaceholder=true", () => {
    render(<Card showPlaceholder />);
    expect(screen.queryByRole("img")).toBeNull();
    const plus = screen.getByText("+");
    expect(plus).toBeInTheDocument();
  });

  it("does not call onClick when disabled and has tabIndex -1", () => {
    const onClick = vi.fn();
    render(<Card image="00-help.png" isDisabled onClick={onClick} />);
    const btn = screen.getByRole("button");
    expect(btn).toHaveAttribute("tabindex", "-1");
    fireEvent.click(btn);
    expect(onClick).not.toHaveBeenCalled();
  });

  it("triggers onClick on Enter and Space key when not disabled", () => {
    const onClick = vi.fn();
    render(<Card image="00-help.png" onClick={onClick} />);
    const btn = screen.getByRole("button");

    fireEvent.keyDown(btn, { key: "Enter" });
    expect(onClick).toHaveBeenCalledTimes(1);

    fireEvent.keyDown(btn, { key: " " });
    expect(onClick).toHaveBeenCalledTimes(2);
  });

  it("applies selected styling when isSelected=true", () => {
    render(<Card image="00-help.png" isSelected />);
    const btn = screen.getByRole("button");
    expect(btn.className).toMatch(/ring-2/);
    expect(btn.className).toMatch(/ring-yellow-500/);
  });

  it("falls back to help image on img error", () => {
    render(<Card image="non-existent.png" alt="broken" />);
    const img = screen.getByAltText("broken");
    fireEvent.error(img);
    expect(img.src).toContain("/Cartas/00-help.png");
  });
});
