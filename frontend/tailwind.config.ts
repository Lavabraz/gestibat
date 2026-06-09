import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
      colors: {
        primary: "#007179",
        "primary-dark": "#005a60",
        "bg-global": "#d9d9d9",
        "card-bg": "#e2e2e2",
        "alert-red": "#ff0004",
        "alert-orange": "#ff7b00",
        "alert-green": "#0de218",
      },
      borderRadius: {
        card: "20px",
        input: "15px",
      },
    },
  },
  plugins: [],
} satisfies Config;
