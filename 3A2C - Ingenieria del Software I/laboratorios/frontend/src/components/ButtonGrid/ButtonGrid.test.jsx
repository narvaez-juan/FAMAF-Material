import { render, screen } from "@testing-library/react";
import ButtonGrid from "./ButtonGrid";

describe("ButtonGrid", () => {
  it("renderiza la cantidad correcta de botones", () => {
    const buttons = [
      { buttonText: "A", buttonActive: true },
      { buttonText: "B", buttonActive: true },
      { buttonText: "C", buttonActive: true },
    ];
    render(<ButtonGrid buttons={buttons} />);
    expect(screen.getAllByRole("button")).toHaveLength(3);
  });
});
