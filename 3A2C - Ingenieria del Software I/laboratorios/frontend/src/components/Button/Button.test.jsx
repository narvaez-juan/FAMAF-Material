import { describe, it, expect, vi } from "vitest";
import "@testing-library/jest-dom";
import { render, screen, fireEvent } from "@testing-library/react";
import Button from "./Button";

describe("Button component", () => {
  it("renderiza el texto correctamente", () => {
    render(<Button buttonText="Click me" />);
    const btn = screen.getByRole("button", { name: "Click me" });
    expect(btn).toBeInTheDocument();
  });

  it("aplica el color de fondo correctamente", () => {
    render(<Button buttonText="Color test" buttonColor="red" />);
    const btn = screen.getByRole("button");
    expect(btn).toHaveStyle({ background: "red" });
  });

  it("cambia el color de fondo y texto al hacer hover", () => {
    render(
      <Button
        buttonText="Hover test"
        buttonColor="blue"
        buttonHoverColor="yellow"
      />
    );
    const btn = screen.getByRole("button");

    fireEvent.mouseOver(btn);
    expect(btn).toHaveStyle({ background: "yellow", color: "rgb(0, 0, 0)" });

    fireEvent.mouseOut(btn);
    expect(btn).toHaveStyle({
      background: "blue",
      color: "rgb(255, 255, 255)",
    });
  });

  it("llama a onClickHandler al hacer clic si no está deshabilitado", () => {
    const onClick = vi.fn();
    render(<Button buttonText="Click test" onClickHandler={onClick} />);
    const btn = screen.getByRole("button");

    fireEvent.click(btn);
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it("no llama a onClickHandler si está deshabilitado", () => {
    const onClick = vi.fn();
    render(
      <Button
        buttonText="Disabled"
        onClickHandler={onClick}
        onDisabledHandler={true}
      />
    );
    const btn = screen.getByRole("button");
    expect(btn).toBeDisabled();

    fireEvent.click(btn);
    expect(onClick).not.toHaveBeenCalled();
  });

  it("combina las clases pasadas por props con las clases base", () => {
    render(<Button buttonText="Styled" className="bg-green-500" />);
    const btn = screen.getByRole("button");
    expect(btn.className).toMatch(/bg-green-500/);
    expect(btn.className).toMatch(/font-metamorphous/);
  });
});
