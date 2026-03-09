import {
  render,
  screen,
  fireEvent,
  waitFor,
  cleanup,
} from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { vi, describe, it, expect, beforeEach, afterEach } from "vitest";
import getSocket from "../../services/WSServices";
import OponentSecrets from "./OponentSecrets";

// Mock de los servicios
vi.mock("../../services/WSServices");
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useParams: () => ({ gameId: "game-456" }),
  };
});

describe("OponentSecrets Component", () => {
  let mockSocket;

  beforeEach(() => {
    // Limpiar localStorage antes de cada test
    localStorage.clear();

    // Mock del socket
    mockSocket = {
      on: vi.fn(),
      off: vi.fn(),
      emit: vi.fn(),
    };
    getSocket.mockResolvedValue(mockSocket);
  });

  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
    localStorage.clear();
  });

  const renderComponent = (props = {}) => {
    return render(
      <BrowserRouter>
        <OponentSecrets
          jugador={{ id_jugador: "player-1", nombre: "Player 1" }}
          playerId={"player-2"}
        />
      </BrowserRouter>
    );
  };

  describe("Renderizado inicial", () => {
    it("debería renderizar el botón de See Secrets", () => {
      renderComponent();
      expect(
        screen.getByRole("button", { name: /See Secrets/i })
      ).toBeInTheDocument();
    });

    it("debería renderizar el botón con estilos correctos", () => {
      renderComponent();
      const button = screen.getByRole("button", { name: /Secrets/i });

      expect(button).toHaveClass(
        "w-full mt-2 px-3 py-1.5 rounded-lg text-sm font-metamorphous font-semibold transition-all duration-200 border border-yellow-600/50 hover:border-yellow-400 shadow-[0_0_4px_rgba(194,162,45,0.3)] hover:shadow-[0_0_8px_rgba(194,162,45,0.6)]"
      );
      expect(button).toHaveStyle({ background: "rgb(11, 59, 111)" });
    });

    it("no debería mostrar el modal inicialmente", () => {
      renderComponent();
      expect(screen.queryByText("Close")).not.toBeInTheDocument();
    });
  });

  describe("Conexión de WebSocket", () => {
    it("debería conectar el socket y configurar listeners", async () => {
      renderComponent();

      await waitFor(() => {
        expect(getSocket).toHaveBeenCalled();
        expect(mockSocket.on).toHaveBeenCalledWith(
          "connect",
          expect.any(Function)
        );
        expect(mockSocket.on).toHaveBeenCalledWith(
          "player_secrets",
          expect.any(Function)
        );
      });
    });

    it("debería emitir get_secrets cuando el socket se conecta", async () => {
      renderComponent();

      await waitFor(() => {
        const connectCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "connect"
        )[1];

        connectCallback();

        expect(mockSocket.emit).toHaveBeenCalledWith(
          "get_secrets",
          "game-456",
          "player-1"
        );
      });
    });

    it("debería guardar gameId en localStorage si no existe RoomID", async () => {
      renderComponent();

      await waitFor(() => {
        expect(localStorage.getItem("RoomID")).toBe("game-456");
      });
    });

    it("no debería sobrescribir RoomID si ya existe en localStorage", async () => {
      localStorage.setItem("RoomID", "existing-room");

      renderComponent();

      await waitFor(() => {
        expect(localStorage.getItem("RoomID")).toBe("existing-room");
      });
    });

    it("debería manejar errores de conexión del socket", async () => {
      const consoleErrorSpy = vi
        .spyOn(console, "error")
        .mockImplementation(() => {});
      getSocket.mockRejectedValue(new Error("Connection failed"));

      renderComponent();

      await waitFor(() => {
        expect(consoleErrorSpy).toHaveBeenCalledWith(
          "Socket connection failed:",
          expect.any(Error)
        );
      });

      consoleErrorSpy.mockRestore();
    });
  });

  describe("Manejo de secretos (handleSecretPayload)", () => {
    it("debería manejar player_secrets de un solo jugador", async () => {
      renderComponent();

      const getSecretPayload = {
        player_id: "player-1",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: false },
          { id: "secret-2", image: "secret2.png", isRevealed: true },
        ],
      };

      await waitFor(() => {
        const initialSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        initialSecretCallback(getSecretPayload);
      });

      // Abrir modal para ver los secretos
      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      await waitFor(() => {
        expect(screen.getAllByAltText(/Secret/i)).toHaveLength(2);
      });
    });

    it("debería mostrar los secretos del jugador Oponente dados vuelta (ocultos)", async () => {
      renderComponent();

      const oponentSecretPayload = {
        player_id: "player-1",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: false },
          { id: "secret-2", image: "secret2.png", isRevealed: false },
          { id: "secret-3", image: "secret3.png", isRevealed: false },
        ],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        playerSecretCallback(oponentSecretPayload);
      });

      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      await waitFor(() => {
        expect(screen.getAllByAltText(/Secret/i)).toHaveLength(3);

        const hiddenImages = screen.getAllByRole("img");

        hiddenImages.forEach((img) => {
          expect(img).toHaveAttribute("src", "/Cartas/05-secret_front.png");
        });
      });
    });

    it("debería mostrar los secretos del jugador Oponente expuestos", async () => {
      renderComponent();

      const oponentSecretPayload = {
        player_id: "player-1",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: true },
          { id: "secret-2", image: "secret2.png", isRevealed: true },
          { id: "secret-3", image: "secret3.png", isRevealed: true },
        ],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        playerSecretCallback(oponentSecretPayload);
      });

      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      const expectedSrcs = [
        "/Cartas/secret1.png",
        "/Cartas/secret2.png",
        "/Cartas/secret3.png",
      ].sort();

      const actualSrcs = screen
        .getAllByRole("img")
        .map((img) => img.getAttribute("src"))
        .sort();

      expect(actualSrcs).toEqual(expectedSrcs);
    });
  });

  describe("Funcionalidad del Modal", () => {
    it("debería abrir el modal al hacer clic en el botón See Secrets", async () => {
      renderComponent();

      const secretPayload = [
        {
          player_id: "player-1",
          secrets_list: [
            { id: "secret-1", image: "secret1.png", isRevealed: false },
          ],
        },
      ];

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        if (playerSecretCallback) {
          playerSecretCallback(secretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      expect(screen.getByText("Close")).toBeInTheDocument();
      expect(
        screen.getByRole("heading", { name: /Secrets/i })
      ).toBeInTheDocument();
    });

    it("debería cerrar el modal al hacer clic en el botón Cerrar", async () => {
      renderComponent();

      const playerSecretPayload = {
        player_id: "player-1",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: false },
        ],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        if (playerSecretCallback) {
          playerSecretCallback(playerSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      const closeButton = screen.getByRole("button", { name: /Close/i });
      fireEvent.click(closeButton);

      expect(screen.queryByText("Close")).not.toBeInTheDocument();
    });

    it("debería cerrar el modal al hacer clic en el backdrop", async () => {
      renderComponent();

      const playerSecretPayload = {
        player_id: "player-1",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: false },
        ],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        if (playerSecretCallback) {
          playerSecretCallback(playerSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      const backdrop = document.querySelector(
        ".absolute.inset-0.bg-black\\/80"
      );

      if (backdrop) {
        fireEvent.click(backdrop);
        await waitFor(() => {
          expect(screen.queryByText("Close")).not.toBeInTheDocument();
        });
      }
    });

    it("debería mostrar los secretos en el modal", async () => {
      renderComponent();

      const playerSecretPayload = {
        player_id: "player-1",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: false },
          { id: "secret-2", image: "secret2.png", isRevealed: true },
          { id: "secret-3", image: "secret3.png", isRevealed: false },
        ],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        if (playerSecretCallback) {
          playerSecretCallback(playerSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      await waitFor(() => {
        expect(screen.getAllByAltText(/Secret/i)).toHaveLength(3);
      });
    });

    it("debería mostrar el header del modal con el icono con la inicial del jugador", async () => {
      renderComponent();

      const playerSecretPayload = {
        player_id: "player-1",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: false },
        ],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        if (playerSecretCallback) {
          playerSecretCallback(playerSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      expect(screen.getByText("P")).toBeInTheDocument();
      expect(
        screen.getByRole("heading", { name: /Secrets/i })
      ).toBeInTheDocument();
    });

    it("debería aplicar grid layout a los secretos", async () => {
      renderComponent();

      const playerSecretPayload = {
        player_id: "player-1",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: false },
        ],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        if (playerSecretCallback) {
          playerSecretCallback(playerSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      const gridContainer = document.querySelector(
        ".grid.grid-cols-1.sm\\:grid-cols-2.md\\:grid-cols-3"
      );

      expect(gridContainer).toBeInTheDocument();
      expect(gridContainer).toHaveClass(
        "grid-cols-1",
        "sm:grid-cols-2",
        "md:grid-cols-3"
      );
    });

    it("debería mostrar mensaje cuando no hay secretos", () => {
      renderComponent();

      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      expect(
        screen.getByText("This player dont have secrets")
      ).toBeInTheDocument();
    });
  });

  describe("Estilos y efectos hover del botón Secrets", () => {
    it("debería cambiar estilos al pasar el mouse sobre el botón", () => {
      renderComponent();
      const button = screen.getByRole("button", { name: /See Secrets/i });

      // Estado inicial
      expect(button).toHaveStyle({ background: "rgb(11, 59, 111)" });

      // Hover
      fireEvent.mouseOver(button);
      expect(button).toHaveStyle({
        background: "rgb(194, 162, 45)",
        color: "rgb(0, 0, 0)",
      });

      // Mouse out
      fireEvent.mouseOut(button);
      expect(button).toHaveStyle({
        background: "rgb(11, 59, 111)",
        color: "rgb(255, 255, 255)",
      });
    });
  });

  describe("Estilos y efectos hover del botón Cerrar", () => {
    it("debería aplicar efecto de brillo al botón Cerrar en hover", async () => {
      renderComponent();

      // Cargar secretos
      const initialSecretPayload = [
        {
          player_id: "player-1",
          secrets_list: [
            { id: "secret-1", image: "secret1.png", isRevealed: false },
          ],
        },
      ];

      await waitFor(() => {
        const initialSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "initial_secrets"
        )?.[1];

        if (initialSecretCallback) {
          initialSecretCallback(initialSecretPayload);
        }
      });

      // Abrir modal
      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      const closeButton = screen.getByRole("button", { name: /Close/i });

      // Estado inicial
      expect(closeButton).toHaveStyle({
        background: "rgb(194, 162, 45)",
        color: "rgb(0, 0, 0)",
      });

      // Hover
      fireEvent.mouseOver(closeButton);
      expect(closeButton).toHaveStyle({ filter: "brightness(0.95)" });

      // Mouse out
      fireEvent.mouseOut(closeButton);
      expect(closeButton).toHaveStyle({ filter: "none" });
    });
  });

  describe("Estado sin secretos", () => {
    it("debería manejar correctamente cuando no hay secretos", async () => {
      renderComponent();

      const playerSecretPayload = {
        player_id: "player-1",
        secrets_list: [],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        playerSecretCallback(playerSecretPayload);
      });

      // Abrir modal
      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      // No debería haber secretos renderizados
      expect(screen.queryByAltText("Secret")).not.toBeInTheDocument();
      expect(
        screen.getByText("This player dont have secrets")
      ).toBeInTheDocument();
    });
  });

  describe("Renderizado de secretos con diferentes estados", () => {
    it("debería renderizar secretos revelados y no revelados", async () => {
      renderComponent();

      const playerSecretPayload = {
        player_id: "player-1",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: true },
          { id: "secret-2", image: "secret2.png", isRevealed: false },
        ],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        playerSecretCallback(playerSecretPayload);
      });

      // Abrir modal
      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      await waitFor(() => {
        expect(screen.getAllByAltText(/Secret/i)).toHaveLength(2);
      });
    });
  });

  describe("Accesibilidad del modal", () => {
    it("debería tener z-index apropiado para el modal", async () => {
      renderComponent();

      const playerSecretPayload = {
        player_id: "player-1",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: false },
        ],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        if (playerSecretCallback) {
          playerSecretCallback(playerSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      const modalBackdrop = screen.getByText("Close").closest(".fixed.inset-0");
      expect(modalBackdrop).toHaveClass("z-50");
    });

    it("debería tener backdrop blur aplicado", async () => {
      renderComponent();

      const playerSecretPayload = {
        player_id: "player-1",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: false },
        ],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        if (playerSecretCallback) {
          playerSecretCallback(playerSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", {
        name: /See Secrets/i,
      });
      fireEvent.click(secretsButton);

      const backdrop = document.querySelector(
        ".absolute.inset-0.bg-black\\/80"
      );
      expect(backdrop).toHaveClass("backdrop-blur-sm");
    });
  });
});
