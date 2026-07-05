// vite.config.js — Vite build tool configuration: plugins (React), dev server settings, proxy rules for backend API, and build options
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
});