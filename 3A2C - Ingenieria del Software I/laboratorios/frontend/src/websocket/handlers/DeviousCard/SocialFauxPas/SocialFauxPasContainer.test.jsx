import { describe, it, expect, vi, beforeEach } from "vitest";
import { handleDeviousCard } from "./SocialFauxPasContainer";
import { handleSocialFauxPas } from "./SocialFauxPasContainer";
import { useEventCardStore } from "../../../../Store/useEventCardStore";
import { emitSecrets } from "../../../../services/WSServices";

// Mock del toast
vi.mock("react-hot-toast", () => {
  const toastFn = vi.fn();
  toastFn.success = vi.fn();
  toastFn.error = vi.fn();
  toastFn.remove = vi.fn();
  toastFn.dismiss = vi.fn();
  return { __esModule: true, default: toastFn };
});

import toast from "react-hot-toast";

// Mock del socket
vi.mock("../../../../services/WSServices", () => ({
  emitSecrets: vi.fn(),
}));

// Mock del store EventCard
vi.mock("../../../../Store/useEventCardStore", () => ({
  useEventCardStore: {
    getState: vi.fn(),
  },
}));

describe("DeviousCardHandler", () => {
  let payload, mockSetVotedToReveal, mockSetVotedPlayerId, mockSetSecrets;

  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();

    mockSetVotedToReveal = vi.fn();
    mockSetVotedPlayerId = vi.fn();
    mockSetSecrets = vi.fn();

    useEventCardStore.getState.mockReturnValue({
      setVotedToReveal: mockSetVotedToReveal,
      setVotedPlayerId: mockSetVotedPlayerId,
      setSecrets: mockSetSecrets,
    });

    payload = {
      player_id: 1,
      source_card: "Social Faux Pas",
      game_id: "G123",
    };
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  describe("handleDeviousCard", () => {
    it("no hace nada si el payload.player_id no coincide con playerId", () => {
      handleDeviousCard(payload, 2);

      expect(toast.dismiss).not.toHaveBeenCalled();
      expect(mockSetVotedToReveal).not.toHaveBeenCalled();
    });

    it("llama a handleSocialFauxPas si source_card es 'Social Faux Pas' y el jugador coincide", () => {
      handleDeviousCard(payload, 1);

      // Avanzar los timers para que se ejecute el setTimeout
      vi.runAllTimers();

      expect(toast.dismiss).toHaveBeenCalledWith("social-faux-pas-1");
      expect(toast).toHaveBeenCalledWith(
        "You received the 'Social Faux Pas' card! You must reveal a secret of your choice.",
        {
          icon: "❗",
          id: "social-faux-pas-1",
        }
      );
      expect(mockSetSecrets).toHaveBeenCalledWith(null);
      expect(emitSecrets).toHaveBeenCalledWith("G123", 1);
      expect(mockSetVotedPlayerId).toHaveBeenCalledWith(1);
      expect(mockSetVotedToReveal).toHaveBeenCalledWith(true);
    });

    it("no llama a handleSocialFauxPas si source_card no es 'Social Faux Pas'", () => {
      payload.source_card = "Other Card";

      handleDeviousCard(payload, 1);

      expect(toast.dismiss).not.toHaveBeenCalled();
      expect(mockSetVotedToReveal).not.toHaveBeenCalled();
    });
  });

  describe("handleSocialFauxPas", () => {
    it("limpia secretos, emite petición y abre modal correctamente", () => {
      handleSocialFauxPas(payload, 1);

      // Verificar que se dismissea el toast
      expect(toast.dismiss).toHaveBeenCalledWith("social-faux-pas-1");

      // Avanzar el setTimeout
      vi.runAllTimers();

      // Verificar que se muestra el toast
      expect(toast).toHaveBeenCalledWith(
        "You received the 'Social Faux Pas' card! You must reveal a secret of your choice.",
        {
          icon: "❗",
          id: "social-faux-pas-1",
        }
      );

      // Verificar que se limpian los secretos ANTES de emitir
      expect(mockSetSecrets).toHaveBeenCalledWith(null);

      // Verificar que se emiten los secretos
      expect(emitSecrets).toHaveBeenCalledWith("G123", 1);

      // Verificar que se setea el playerId
      expect(mockSetVotedPlayerId).toHaveBeenCalledWith(1);

      // Verificar que se abre el modal
      expect(mockSetVotedToReveal).toHaveBeenCalledWith(true);
    });

    it("usa el playerId correcto en todas las llamadas", () => {
      const customPayload = {
        player_id: 5,
        source_card: "Social Faux Pas",
        game_id: "G999",
      };

      handleSocialFauxPas(customPayload, 5);

      vi.runAllTimers();

      expect(toast.dismiss).toHaveBeenCalledWith("social-faux-pas-5");
      expect(toast).toHaveBeenCalledWith(
        "You received the 'Social Faux Pas' card! You must reveal a secret of your choice.",
        {
          icon: "❗",
          id: "social-faux-pas-5",
        }
      );
      expect(emitSecrets).toHaveBeenCalledWith("G999", 5);
      expect(mockSetVotedPlayerId).toHaveBeenCalledWith(5);
      expect(mockSetVotedToReveal).toHaveBeenCalledWith(true);
    });
  });
});
