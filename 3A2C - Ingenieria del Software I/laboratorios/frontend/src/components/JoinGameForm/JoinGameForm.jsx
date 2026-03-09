import { useState } from "react";

export default function PlayerForm({ gameId, onSubmit }) {
  const [formData, setFormData] = useState({
    player_name: "",
    player_birth_date: "",
  });

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
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  };

  const validateField = (name, value) => {
    let error = "";

    switch (name) {
      case "player_name":
        if (!value.trim()) error = "Player name is required";
        break;
      case "player_birth_date":
        if (!value.trim()) error = "Player birth date is required";
        break;
      default:
        break;
    }

    return error;
  };
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
    setFormData((_) => ({
      player_name: getRandomPlayerName(),
      player_birth_date: randomDateMoreThan20YearsAgo(new Date(1900, 0, 1)),
    }));
    setErrors({});
  };

  const resetForm = () => {
    setFormData({
      player_name: "",
      player_birth_date: "",
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
      await onSubmit(formData, gameId);
      resetForm();
    } catch (error) {
      console.error("Error submitting form:", error);
      alert("Failed to submit form: " + error.message);
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
            type="submit"
            className="inline-flex items-center px-20 py-2 text-white rounded-md focus:outline-none"
            style={{ background: "#0b3b6f" }}
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
            {isSubmitting ? "Submitting..." : "Submit"}
          </button>

          <button
            type="button"
            className="inline-flex items-center px-20 py-2 text-white rounded-md focus:outline-none"
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
            Autocompletar
          </button>
        </div>
      </div>
    </form>
  );
}
