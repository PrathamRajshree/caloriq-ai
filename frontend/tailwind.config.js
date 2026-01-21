export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      animation: {
        glow: "glow 2s ease-in-out infinite",
      },
      keyframes: {
        glow: {
          "0%, 100%": { boxShadow: "0 0 20px #6366f1" },
          "50%": { boxShadow: "0 0 40px #a855f7" },
        },
      },
    },
  },
  plugins: [],
}
