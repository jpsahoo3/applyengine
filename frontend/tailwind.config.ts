import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#111111",
        wheat: "#f4ecd8",
        ember: "#d96f32",
        moss: "#37503b",
        fog: "#d8d6cf"
      },
      fontFamily: {
        display: ["Space Grotesk", "Segoe UI", "sans-serif"],
        body: ["IBM Plex Sans", "Segoe UI", "sans-serif"]
      },
      boxShadow: {
        panel: "0 20px 60px rgba(17, 17, 17, 0.12)"
      }
    }
  },
  plugins: []
};

export default config;

