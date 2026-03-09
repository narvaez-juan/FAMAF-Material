import {
  render,
  screen,
  fireEvent,
  waitFor,
  cleanup,
} from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { vi, describe, it, expect, beforeEach, afterEach } from "vitest";

import OponentSets from "./OponentSets";

let mockFetchPlayerSets;
let mockRequestedPlayerSets;

vi.mock("../../containers/GameLogic/PlaySetContainer", () => {
  return {
    __esModule: true,
    default: (gameId, playerId) => {
      return {
        requestedPlayerSets: mockRequestedPlayerSets,
        fetchPlayerSets: mockFetchPlayerSets,
      };
    },
  };
});

vi.mock("../Card/Card", () => ({
  __esModule: true,
  default: ({ image, alt }) => (
    <img data-testid="set-card" src={image} alt={alt} />
  ),
}));

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useParams: () => ({ gameId: "game-456" }),
  };
});

describe("OponentSets Component", () => {
  const jugadorFixture = { id_jugador: 101, nombre: "Player 1" };

  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();
    mockFetchPlayerSets = vi.fn();
    mockRequestedPlayerSets = [];
  });

  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
    localStorage.clear();
  });

  const renderComponent = (props = {}) => {
    return render(
      <BrowserRouter>
        <OponentSets jugador={jugadorFixture} playerId={202} {...props} />
      </BrowserRouter>
    );
  };

  it("debería renderizar el botón 'See Sets' inicialmente", () => {
    renderComponent();
    expect(
      screen.getByRole("button", { name: /See Sets/i })
    ).toBeInTheDocument();
  });

  it("no debería mostrar el modal inicialmente", () => {
    renderComponent();
    expect(screen.queryByText("Close")).not.toBeInTheDocument();
  });

  it("al hacer click en el botón llama a fetchPlayerSets con el id del jugador y abre modal (sin sets)", async () => {
    renderComponent();

    const btn = screen.getByRole("button", { name: /See Sets/i });
    fireEvent.click(btn);

    expect(mockFetchPlayerSets).toHaveBeenCalledWith(jugadorFixture.id_jugador);

    await waitFor(() => {
      expect(
        screen.getByText(
          /This player.?s? ?doesn.?t? have sets|This player.*have sets/i
        )
      ).toBeInTheDocument();
    });

    expect(screen.getByText(/0 sets/)).toBeInTheDocument();
  });

  it("debería renderizar las imágenes de los sets cuando requestedPlayerSets tiene datos", async () => {
    mockRequestedPlayerSets = [
      {
        set_play_id: "set-1",
        card_game_images: ["imgA.png", "imgB.png"],
        card_game_ids: [11, 12],
      },
      {
        set_play_id: "set-2",
        card_game_images: ["imgC.png"],
        card_game_ids: [21],
      },
    ];

    renderComponent();

    const btn = screen.getByRole("button", { name: /See Sets/i });
    fireEvent.click(btn);

    await waitFor(() => {
      const imgs = screen.getAllByTestId("set-card");
      expect(imgs).toHaveLength(3);
      const srcs = imgs.map((i) => i.getAttribute("src")).sort();
      expect(srcs).toEqual(["imgA.png", "imgB.png", "imgC.png"].sort());
    });

    expect(screen.getByText(/2 sets/)).toBeInTheDocument();
  });

  it("debería cerrar el modal al hacer click en el botón Close", async () => {
    mockRequestedPlayerSets = [
      {
        set_play_id: "set-1",
        card_game_images: ["imgA.png"],
        card_game_ids: [11],
      },
    ];
    renderComponent();

    const openBtn = screen.getByRole("button", { name: /See Sets/i });
    fireEvent.click(openBtn);

    await waitFor(() => {
      expect(screen.getByText("Close")).toBeInTheDocument();
    });

    const closeBtn = screen.getByRole("button", { name: /Close/i });
    fireEvent.click(closeBtn);

    await waitFor(() => {
      expect(screen.queryByText("Close")).not.toBeInTheDocument();
    });
  });

  it("debería mostrar la inicial del jugador en el header del modal", async () => {
    mockRequestedPlayerSets = [
      {
        set_play_id: "set-1",
        card_game_images: ["imgA.png"],
        card_game_ids: [11],
      },
    ];
    renderComponent();

    const openBtn = screen.getByRole("button", { name: /See Sets/i });
    fireEvent.click(openBtn);

    await waitFor(() => {
      expect(screen.getByText("P")).toBeInTheDocument();
    });

    expect(
      screen.getByRole("heading", { name: /Sets of Player 1/i })
    ).toBeInTheDocument();
  });

  it("debería mostrar mensaje si requestedPlayerSets está vacío", async () => {
    mockRequestedPlayerSets = [];
    renderComponent();

    const openBtn = screen.getByRole("button", { name: /See Sets/i });
    fireEvent.click(openBtn);

    await waitFor(() => {
      expect(
        screen.getByText(
          /This player.?s? ?doesn.?t? have sets|This player.*have sets/i
        )
      ).toBeInTheDocument();
    });
  });
});
