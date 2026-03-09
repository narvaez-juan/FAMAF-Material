import { render, screen } from "@testing-library/react";
import StatusMessage from "./StatusMessage";

describe("StatusMessage", () => {
  it("renders the message with default color", () => {
    render(<StatusMessage message="Hello World" />);
    expect(screen.getByText("Hello World")).toBeInTheDocument();
    expect(screen.getByText("Hello World")).toHaveClass("text-white");
  });

  it("renders the message with red color", () => {
    render(<StatusMessage message="Error!" color="red" />);
    expect(screen.getByText("Error!")).toHaveClass("text-red-500");
  });

  it("renders the message with yellow color", () => {
    render(<StatusMessage message="Warning!" color="yellow" />);
    expect(screen.getByText("Warning!")).toHaveClass("text-yellow-400");
  });
});
