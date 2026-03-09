import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
//import '@testing-library/jest-dom/vitest';

export default defineConfig({
  plugins: [tailwindcss(), react()],
  server: {
    port: 3000,
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "/setupTests.js",
    silent: true,
    onConsoleLog(log, type) {
      return false;
    },
    onStdout() {
      return false;
    },
    onStderr() {
      return false;
    },
  },
});
