import { render, screen, fireEvent, act } from "@testing-library/react";
import { vi } from "vitest";
import SelectDirectionModal from "./SelectDirectionModal";
import { useEventCardStore } from "../../Store/useEventCardStore";
import { useDeadCardFollyStore } from "../../Store/DeadCardFollyStore";

vi.mock("../../Store/DeadCardFollyStore", () => ({
  useDeadCardFollyStore: vi.fn(),
}));

describe("SelectDirectionModal", () => {
  const setSelectedDirection = vi.fn();
  const setSelectDirection = vi.fn();

  beforeEach(() => {
    vi.useFakeTimers();
    useDeadCardFollyStore.mockReturnValue({
      setSelectedDirection,
      setSelectDirection,
    });
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  test("renders directions and initial info text", () => {
    render(<SelectDirectionModal />);

    expect(screen.getByText(/Select Direction/i)).toBeInTheDocument();
    expect(screen.getByText(/seconds left/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Left/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Right/i })).toBeInTheDocument();

    const confirmButton = screen.getByRole("button", { name: /Confirm/i });
    expect(confirmButton).toBeDisabled();
  });

  test("selecting a direction enables confirm button and calls store on confirm", () => {
    render(<SelectDirectionModal />);

    const leftButton = screen.getByRole("button", { name: /Left/i });
    fireEvent.click(leftButton);

    const confirmButton = screen.getByRole("button", { name: /Confirm/i });
    expect(confirmButton).not.toBeDisabled();

    fireEvent.click(confirmButton);
    expect(setSelectedDirection).toHaveBeenCalledWith("left");
    expect(setSelectDirection).toHaveBeenCalledWith(false);
  });

  test("auto-selects random direction after 5 seconds", () => {
    render(<SelectDirectionModal />);

    act(() => {
      vi.advanceTimersByTime(5000);
    });

    expect(setSelectedDirection).toHaveBeenCalled();
    expect(setSelectDirection).toHaveBeenCalledWith(false);
  });

  test("info text countdown decreases every second", () => {
    render(<SelectDirectionModal />);

    expect(screen.getByText(/5 seconds left/i)).toBeInTheDocument();

    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(screen.getByText(/4 seconds left/i)).toBeInTheDocument();

    act(() => {
      vi.advanceTimersByTime(3000);
    });
    expect(screen.getByText(/1 seconds left/i)).toBeInTheDocument();
  });
});
