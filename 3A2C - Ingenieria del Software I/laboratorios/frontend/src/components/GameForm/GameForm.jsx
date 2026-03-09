import { useState } from "react";

export default function GameForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    game_name: "",
    min_players: "",
    max_players: "",
    player_name: "",
    player_birth_date: "",
  });

  const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      if (name == "min_players" || name == "max_players") {
        setErrors((prev) => ({
          ...prev,
          ["range_error"]: "",
          [name]: "",
        }));
      } else {
        setErrors((prev) => ({
          ...prev,
          [name]: "",
        }));
      }
    }
  };

  const validateField = (name, value) => {
    let error = "";

    switch (name) {
      case "game_name":
        if (!value.trim()) error = "Game name is required";
        break;
      case "min_players":
        if (!value.trim()) error = "Minimum number of players is required";
        break;
      case "max_players":
        if (!value.trim()) error = "Maximum number of players is required";
        break;
      case "player_name":
        if (!value.trim()) error = "Player name is required";
        break;
      case "player_birth_date":
        if (!value.trim()) {
          error = "Player birth date is required";
        } else if (!dateRegex.test(value)) {
          error = "Invalid date format";
        } else {
          const d = new Date(value);
          if (isNaN(d.getTime())) {
            error = "Invalid date";
          }
        }
      default:
        break;
    }

    return error;
  };

  function getRandomGameName() {
    const prefixes = [
      "Versalles",
      "Fire",
      "Pueblo",
      "Ciudada",
      "Continent",
      "La Punta",
    ];
    const suffixes = [
      "Pit",
      "Del C#&o",
      "Narnia",
      "Carajo",
      "Guadalajara",
      "Guatemala",
    ];
    const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
    const suffix = suffixes[Math.floor(Math.random() * suffixes.length)];
    return `${prefix} ${suffix}`;
  }

  function getRandomPlayerName() {
    const firstNames = [
      "Pedro",
      "Maladroga",
      "Mister",
      "LaNaranja",
      "JERE",
      "Mirta",
      "Mario",
      "Luigi",
      "Pepito",
      "Porquien",
      "Kylian",
      "Testos",
      "Elpan",
      "Micro",
      "Fideo",
      "Arroz",
    ];
    const lastNames = [
      "Pascal",
      "Orange",
      "Mecanica",
      "De Izquierda",
      "Milei",
      "Luigi",
      "Mario",
      "Verstappen",
      "Perez",
      "Porhonga",
      "Mbappe",
      "Terona",
      "Cito",
      "Macro",
      "Dimaria",
      "ConTuco",
    ];
    const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
    const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
    return `${firstName} ${lastName}`;
  }

  function randomDateMoreThan20YearsAgo(start = new Date(1900, 0, 1)) {
    const end = new Date();
    end.setFullYear(end.getFullYear() - 20);

    const randomMs =
      start.getTime() + Math.random() * (end.getTime() - start.getTime());
    const d = new Date(randomMs);

    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, "0");
    const dd = String(d.getDate()).padStart(2, "0");

    return `${yyyy}-${mm}-${dd}`;
  }

  const randomData = () => {
    setFormData({
      game_name: getRandomGameName(),
      min_players: "2",
      max_players: "6",
      player_name: getRandomPlayerName(),
      player_birth_date: randomDateMoreThan20YearsAgo(new Date(1900, 0, 1)),
    });
    setErrors({});
  };

  const validateForm = () => {
    const newErrors = {};

    // Validate all required fields
    Object.keys(formData).forEach((key) => {
      const error = validateField(key, formData[key]);
      if (error) {
        newErrors[key] = error;
      }
    });

    const min_players = formData.min_players;
    const max_players = formData.max_players;

    if (min_players) {
      if (min_players < 2 || min_players > 6) {
        const error = "Minimum number of players must be between 2 and 6";
        newErrors.min_players = error;
      }
    }

    if (max_players) {
      if (max_players < 2 || max_players > 6) {
        const error = "Maximum number of players must be between 2 and 6";
        newErrors.max_players = error;
      }
    }

    // Validate min_players and max_players
    if (min_players && max_players) {
      if (min_players > max_players) {
        const error =
          "Minimum number of players must be less than maximum number of players";
        newErrors.range_error = error;
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      await onSubmit(formData);
      setFormData({
        game_name: "",
        min_players: "",
        max_players: "",
        player_name: "",
        player_birth_date: "",
      });
      setErrors({});
    } catch (error) {
      console.error("Error submitting form:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const getInputClassName = (fieldName) => {
    const baseClasses =
      "block w-full px-3 py-2 border rounded-md bg-white/4 text-blue-50 placeholder-blue-200 shadow-sm focus:outline-none";
    const errorClasses = errors[fieldName]
      ? "border-red-500 dark:border-red-400 focus:ring-red-500 dark:focus:ring-red-400"
      : "border-gray-300 dark:border-gray-600 focus:ring-blue-500 dark:focus:ring-blue-400";
    return `${baseClasses} ${errorClasses}`;
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="bg-slate-900 p-6 rounded-md">
        <div className="mb-4">
          <label
            htmlFor="game_name"
            className="block text-sm font-medium text-blue-50 mb-1"
          >
            Game name
          </label>
          <input
            type="text"
            id="game_name"
            name="game_name"
            value={formData.game_name}
            onChange={handleChange}
            required
            className={getInputClassName("game_name")}
            style={{ borderColor: "#0b2340" }}
            placeholder="e.g. Mystery Mansion"
          />
          {errors.game_name && (
            <p className="mt-1 text-sm text-red-600 dark:text-red-400">
              {errors.game_name}
            </p>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="mb-4">
            <label
              htmlFor="min_players"
              className="block text-sm font-medium text-blue-50 mb-1"
            >
              Min players
            </label>
            <input
              type="number"
              id="min_players"
              name="min_players"
              value={formData.min_players}
              onChange={handleChange}
              required
              min="2"
              max="6"
              className={getInputClassName("min_players")}
              style={{ borderColor: "#0b2340" }}
              placeholder="2"
            />
            {errors.min_players && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.min_players}
              </p>
            )}
            {errors.range_error && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.range_error}
              </p>
            )}
          </div>

          <div className="mb-4">
            <label
              htmlFor="max_players"
              className="block text-sm font-medium text-blue-50 mb-1"
            >
              Max players
            </label>
            <input
              type="number"
              id="max_players"
              name="max_players"
              value={formData.max_players}
              onChange={handleChange}
              required
              min="2"
              max="6"
              className={getInputClassName("max_players")}
              style={{ borderColor: "#0b2340" }}
              placeholder="4"
            />
            {errors.max_players && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.max_players}
              </p>
            )}
          </div>
        </div>

        <div className="mb-4">
          <label
            htmlFor="player_name"
            className="block text-sm font-medium text-blue-50 mb-1"
          >
            Player name
          </label>
          <input
            type="text"
            id="player_name"
            name="player_name"
            value={formData.player_name}
            onChange={handleChange}
            required
            className={getInputClassName("player_name")}
            style={{ borderColor: "#0b2340" }}
            placeholder="Your name"
          />
          {errors.player_name && (
            <p className="mt-1 text-sm text-red-600 dark:text-red-400">
              {errors.player_name}
            </p>
          )}
        </div>

        <div className="mb-4">
          <label
            htmlFor="player_birth_date"
            className="block text-sm font-medium text-blue-50 mb-1"
          >
            Player birth date
          </label>
          <input
            type="date"
            id="player_birth_date"
            name="player_birth_date"
            value={formData.player_birth_date}
            onChange={handleChange}
            required
            className={getInputClassName("player_birth_date")}
            style={{ borderColor: "#0b2340" }}
          />
          {errors.player_birth_date && (
            <p className="mt-1 text-sm text-red-600 dark:text-red-400">
              {errors.player_birth_date}
            </p>
          )}
        </div>

        <div className="mt-6 flex justify-between">
          <button
            type={"submit"}
            className={
              "inline-flex items-center px-20 py-2 text-white rounded-md focus:outline-none"
            }
            style={{ background: "#0b3b6f" }}
            onClick={handleSubmit}
            disabled={
              isSubmitting || Object.keys(errors).some((key) => errors[key])
            }
            onMouseOver={(e) => {
              e.currentTarget.style.background = "#c2a22d";
              e.currentTarget.style.color = "black";
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.background = "#0b3b6f";
              e.currentTarget.style.color = "white";
            }}
          >
            {isSubmitting ? "Creating..." : "Create"}
          </button>

          <button
            type={"button"}
            className={
              "inline-flex items-center px-20 py-2 text-white rounded-md focus:outline-none"
            }
            style={{ background: "#0b3b6f" }}
            onClick={randomData}
            disabled={isSubmitting}
            onMouseOver={(e) => {
              e.currentTarget.style.background = "#c2a22d";
              e.currentTarget.style.color = "black";
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.background = "#0b3b6f";
              e.currentTarget.style.color = "white";
            }}
          >
            {"Autocomplete"}
          </button>
        </div>
      </div>
    </form>
  );
}
