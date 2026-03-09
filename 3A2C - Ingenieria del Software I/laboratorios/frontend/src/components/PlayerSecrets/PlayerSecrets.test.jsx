import {
  render,
  screen,
  fireEvent,
  waitFor,
  cleanup,
} from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { vi, describe, it, expect, beforeEach, afterEach } from "vitest";
import PlayerSecret from "./PlayerSecrets";
import getSocket from "../../services/WSServices";

// Mock de los servicios
vi.mock("../../services/WSServices");
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useParams: () => ({ gameId: "game-456" }),
  };
});

describe("PlayerSecret Component", () => {
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
        <PlayerSecret playerId="player-1" {...props} />
      </BrowserRouter>
    );
  };

  describe("Renderizado inicial", () => {
    it("debería renderizar el botón de Secrets", () => {
      renderComponent();
      expect(
        screen.getByRole("button", { name: /Secrets/i })
      ).toBeInTheDocument();
    });

    it("debería renderizar el botón con estilos correctos", () => {
      renderComponent();
      const button = screen.getByRole("button", { name: /Secrets/i });

      expect(button).toHaveClass("fixed", "bottom-6", "right-6", "z-40");
      expect(button).toHaveStyle({ background: "rgb(11, 59, 111)" });
    });

    it("no debería mostrar el modal inicialmente", () => {
      renderComponent();
      expect(screen.queryByText("Cerrar")).not.toBeInTheDocument();
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
          "initial_secrets",
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
    it("debería manejar initial_secrets con array de jugadores", async () => {
      renderComponent();

      const initialSecretPayload = [
        {
          player_id: "player-1",
          secrets_list: [
            { id: "secret-1", image: "secret1.png", isRevealed: false },
            { id: "secret-2", image: "secret2.png", isRevealed: true },
          ],
        },
        {
          player_id: "player-2",
          secrets_list: [
            { id: "secret-3", image: "secret3.png", isRevealed: false },
          ],
        },
      ];

      await waitFor(() => {
        const initialSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "initial_secrets"
        )[1];

        initialSecretCallback(initialSecretPayload);
      });

      // Abrir modal para ver los secretos
      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      await waitFor(() => {
        expect(screen.getAllByAltText("Secret")).toHaveLength(2);
      });
    });

    it("debería filtrar secretos por player_id correcto", async () => {
      renderComponent({ playerId: "player-2" });

      const initialSecretPayload = [
        {
          player_id: "player-1",
          secrets_list: [
            { id: "secret-1", image: "secret1.png", isRevealed: false },
          ],
        },
        {
          player_id: "player-2",
          secrets_list: [
            { id: "secret-2", image: "secret2.png", isRevealed: true },
            { id: "secret-3", image: "secret3.png", isRevealed: false },
          ],
        },
      ];

      await waitFor(() => {
        const initialSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "initial_secrets"
        )[1];

        initialSecretCallback(initialSecretPayload);
      });

      // Abrir modal
      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      await waitFor(() => {
        expect(screen.getAllByAltText("Secret")).toHaveLength(2);
      });
    });

    it("debería manejar player_secrets de un solo jugador", async () => {
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

        playerSecretCallback(playerSecretPayload);
      });

      // Abrir modal
      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      await waitFor(() => {
        expect(screen.getByAltText("Secret")).toBeInTheDocument();
      });
    });

    it("debería ignorar payload de otro jugador", async () => {
      renderComponent({ playerId: "player-1" });

      const playerSecretPayload = {
        player_id: "player-2",
        secrets_list: [
          { id: "secret-1", image: "secret1.png", isRevealed: false },
        ],
      };

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        playerSecretCallback(playerSecretPayload);
      });

      // Abrir modal
      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      // No debería haber secretos
      expect(screen.queryByAltText("Secret")).not.toBeInTheDocument();
      expect(
        screen.getByText("No hay secretos por mostrar.")
      ).toBeInTheDocument();
    });

    it("debería manejar errores en el payload", async () => {
      const consoleErrorSpy = vi
        .spyOn(console, "error")
        .mockImplementation(() => {});

      renderComponent();

      await waitFor(() => {
        const playerSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "player_secrets"
        )[1];

        // Payload inválido que causará error
        playerSecretCallback(null);
      });

      expect(consoleErrorSpy).toHaveBeenCalledWith(
        "Error manejando payload de secretos:",
        expect.any(Error)
      );

      consoleErrorSpy.mockRestore();
    });
  });

  describe("Carga desde localStorage", () => {
    it("debería cargar initialSecrets desde localStorage", async () => {
      const storedData = [
        {
          player_id: "player-1",
          secrets_list: [
            { id: "stored-secret-1", image: "stored1.png", isRevealed: false },
          ],
        },
      ];
      localStorage.setItem("initialSecrets", JSON.stringify(storedData));

      renderComponent();

      // Abrir modal
      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      await waitFor(() => {
        expect(screen.getByAltText("Secret")).toBeInTheDocument();
      });
    });

    it("no debería fallar si no hay datos en localStorage", () => {
      expect(() => renderComponent()).not.toThrow();
    });

    it("debería manejar datos malformados en localStorage", () => {
      localStorage.setItem("initialSecrets", "invalid-json");
      const consoleErrorSpy = vi
        .spyOn(console, "error")
        .mockImplementation(() => {});

      expect(() => renderComponent()).not.toThrow();

      expect(consoleErrorSpy).toHaveBeenCalledWith(
        "initialSecrets parse error:",
        expect.any(Error)
      );

      consoleErrorSpy.mockRestore();
    });
  });

  describe("Funcionalidad del Modal", () => {
    it("debería abrir el modal al hacer clic en el botón Secrets", async () => {
      renderComponent();

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
        )[1];

        if (initialSecretCallback) {
          initialSecretCallback(initialSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      expect(screen.getByText("Cerrar")).toBeInTheDocument();
      expect(
        screen.getByRole("heading", { name: /Secrets/i })
      ).toBeInTheDocument();
    });

    it("debería cerrar el modal al hacer clic en el botón Cerrar", async () => {
      renderComponent();

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
        )[1];

        if (initialSecretCallback) {
          initialSecretCallback(initialSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      const closeButton = screen.getByRole("button", { name: /Cerrar/i });
      fireEvent.click(closeButton);

      expect(screen.queryByText("Cerrar")).not.toBeInTheDocument();
    });

    it("debería cerrar el modal al hacer clic en el backdrop", async () => {
      renderComponent();

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
        )[1];

        if (initialSecretCallback) {
          initialSecretCallback(initialSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      const backdrop = document.querySelector(
        ".absolute.inset-0.bg-black\\/80"
      );

      if (backdrop) {
        fireEvent.click(backdrop);
        await waitFor(() => {
          expect(screen.queryByText("Cerrar")).not.toBeInTheDocument();
        });
      }
    });

    it("debería mostrar los secretos en el modal", async () => {
      renderComponent();

      const initialSecretPayload = [
        {
          player_id: "player-1",
          secrets_list: [
            { id: "secret-1", image: "secret1.png", isRevealed: false },
            { id: "secret-2", image: "secret2.png", isRevealed: true },
            { id: "secret-3", image: "secret3.png", isRevealed: false },
          ],
        },
      ];

      await waitFor(() => {
        const initialSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "initial_secrets"
        )[1];

        if (initialSecretCallback) {
          initialSecretCallback(initialSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      const secrets = screen.getAllByAltText("Secret");
      expect(secrets).toHaveLength(3);
    });

    it("debería mostrar el header del modal con el icono S", async () => {
      renderComponent();

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
        )[1];

        if (initialSecretCallback) {
          initialSecretCallback(initialSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      expect(screen.getByText("S")).toBeInTheDocument();
      expect(
        screen.getByRole("heading", { name: /Secrets/i })
      ).toBeInTheDocument();
    });

    it("debería aplicar grid layout a los secretos", async () => {
      renderComponent();

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
        )[1];

        if (initialSecretCallback) {
          initialSecretCallback(initialSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
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

      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      expect(
        screen.getByText("No hay secretos por mostrar.")
      ).toBeInTheDocument();
    });
  });

  describe("Estilos y efectos hover del botón Secrets", () => {
    it("debería cambiar estilos al pasar el mouse sobre el botón", () => {
      renderComponent();
      const button = screen.getByRole("button", { name: /Secrets/i });

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
      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      const closeButton = screen.getByRole("button", { name: /Cerrar/i });

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

      const initialSecretPayload = [
        {
          player_id: "player-1",
          secrets_list: [],
        },
      ];

      await waitFor(() => {
        const initialSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "initial_secrets"
        )[1];

        initialSecretCallback(initialSecretPayload);
      });

      // Abrir modal
      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      // No debería haber secretos renderizados
      expect(screen.queryByAltText("Secret")).not.toBeInTheDocument();
      expect(
        screen.getByText("No hay secretos por mostrar.")
      ).toBeInTheDocument();
    });
  });

  describe("Renderizado de secretos con diferentes estados", () => {
    it("debería renderizar secretos revelados y no revelados", async () => {
      renderComponent();

      const initialSecretPayload = [
        {
          player_id: "player-1",
          secrets_list: [
            { id: "secret-1", image: "secret1.png", isRevealed: true },
            { id: "secret-2", image: "secret2.png", isRevealed: false },
          ],
        },
      ];

      await waitFor(() => {
        const initialSecretCallback = mockSocket.on.mock.calls.find(
          (call) => call[0] === "initial_secrets"
        )[1];

        initialSecretCallback(initialSecretPayload);
      });

      // Abrir modal
      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      const secrets = screen.getAllByAltText("Secret");
      expect(secrets).toHaveLength(2);
    });
  });

  describe("Accesibilidad del modal", () => {
    it("debería tener z-index apropiado para el modal", async () => {
      renderComponent();

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
        )[1];

        if (initialSecretCallback) {
          initialSecretCallback(initialSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      const modalBackdrop = screen
        .getByText("Cerrar")
        .closest(".fixed.inset-0");
      expect(modalBackdrop).toHaveClass("z-50");
    });

    it("debería tener backdrop blur aplicado", async () => {
      renderComponent();

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
        )[1];

        if (initialSecretCallback) {
          initialSecretCallback(initialSecretPayload);
        }
      });

      const secretsButton = screen.getByRole("button", { name: /Secrets/i });
      fireEvent.click(secretsButton);

      const backdrop = document.querySelector(
        ".absolute.inset-0.bg-black\\/80"
      );
      expect(backdrop).toHaveClass("backdrop-blur-sm");
    });
  });
});
