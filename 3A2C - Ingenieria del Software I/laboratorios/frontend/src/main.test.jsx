import { vi } from "vitest";
import { StrictMode } from "react";
import App from "./containers/App/App.jsx";

const renderMock = vi.fn();
const rootMock = { render: renderMock };

vi.mock("react-dom/client", () => ({
  createRoot: vi.fn(() => rootMock),
}));

const elementMock = {};
vi.spyOn(document, "getElementById").mockReturnValue(elementMock);

describe("main.jsx", () => {
  beforeEach(() => {
    renderMock.mockClear();
  });

  it("renders App inside StrictMode", async () => {
    await import("./main.jsx");
    expect(renderMock).toHaveBeenCalledTimes(1);

    const arg = renderMock.mock.calls[0][0];
    expect(arg.type).toBe(StrictMode);
    expect(arg.props.children.type).toBe(App);
  });
});
