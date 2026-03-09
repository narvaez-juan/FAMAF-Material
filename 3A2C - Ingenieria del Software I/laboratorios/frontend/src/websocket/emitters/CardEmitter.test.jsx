import { describe, it, vi, expect } from "vitest";
import * as WSEmitters from "./CardEmitter";
import * as WSServices from "../../services/WSServices.js";

vi.mock("../../services/WSServices.js", () => ({
  emit: vi.fn(),
}));

describe("CardEmitter", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("emitSelectCard construye payload correctamente y llama a emit", () => {
    WSEmitters.emitSelectCard(
      1,
      42,
      "Dead Card Folly",
      "cardImage.png",
      "left",
      "Event"
    );

    expect(WSServices.emit).toHaveBeenCalledWith("select_card", {
      event: "card_played_event",
      game_id: 1,
      player_id: 42,
      card_name: "Dead Card Folly",
      card_image: "cardImage.png",
      card_type: "Event",
      direction: "left",
    });
  });

  it("resolveSelectCard construye payload correctamente y llama a emit", () => {
    WSEmitters.resolveSelectCard(1, 42, "card99", "cardImg.png", 99);

    expect(WSServices.emit).toHaveBeenCalledWith("resolve_select_card", {
      game_id: 1,
      player_id: 42,
      card_id: "card99",
      card_image: "cardImg.png",
      requester_id: 99,
    });
  });
});
