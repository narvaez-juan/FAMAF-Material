import { render, screen, cleanup } from "@testing-library/react";
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import PlayerSets from "./PlayerSets";

// 🧩 Mock del componente Card (igual que en tu estilo)
vi.mock("../Card/Card", () => ({
  __esModule: true,
  default: ({ image, alt }) => <img data-testid="card" src={image} alt={alt} />,
}));

describe("PlayerSets Component", () => {
  const mockSets = [
    {
      card_game_images: ["img1.png", "img2.png", "img3.png"],
      card_game_ids: [1, 2, 3],
    },
  ];

  beforeEach(() => {
    cleanup();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it("debería renderizar las cartas del último set", () => {
    render(<PlayerSets sets={mockSets} />);

    const cards = screen.getAllByTestId("card");
    expect(cards).toHaveLength(3);
    expect(cards[0]).toHaveAttribute("src", "img1.png");
    expect(cards[1]).toHaveAttribute("src", "img2.png");
    expect(cards[2]).toHaveAttribute("src", "img3.png");
  });

  it("debería usar el alt correcto en las imágenes", () => {
    render(<PlayerSets sets={mockSets} />);
    const cards = screen.getAllByTestId("card");
    cards.forEach((card) => {
      expect(card).toHaveAttribute("alt", "SetCard");
    });
  });

  it("no debería romper si no hay sets", () => {
    const { container } = render(<PlayerSets sets={[]} />);
    expect(container.firstChild).toBeNull();
  });

  it("debería aplicar estilos correctos a las cartas (rotación y posición)", () => {
    render(<PlayerSets sets={mockSets} />);
    const cards = screen.getAllByTestId("card");

    // inspeccionamos los estilos inline que se calculan
    const wrappers = cards.map((card) => card.parentElement);

    wrappers.forEach((wrapper, i) => {
      expect(wrapper).toHaveClass(
        "absolute",
        "transition-transform",
        "duration-300",
        "hover:scale-110"
      );
      expect(wrapper.style.transform).toContain("rotate");
      expect(wrapper.style.left).toContain("px");
    });
  });
});
