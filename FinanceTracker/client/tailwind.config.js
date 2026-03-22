/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                "primary": "#001f3d",
                "accent": "#0bda5b",
                "background-light": "#f5f7f8",
                "background-dark": "#0f1923",
                "card-dark": "#172636",
                "surface-dark": "#16222c",
                "border-dark": "#2e4d6b",
                "accent-success": "#0bda5b",
                "accent-error": "#fa6238",
                "accent-blue": "#007aff",
                "accent-teal": "#00d4ff",
                "accent-green": "#0bda5b",
                "emerald-accent": "#10b981",
                "emerald-hover": "#059669",
            },
            fontFamily: {
                "display": ["Inter", "sans-serif"]
            },
            borderRadius: {
                "DEFAULT": "0.25rem",
                "lg": "0.5rem",
                "xl": "0.75rem",
                "full": "9999px"
            },
        },
    },
    plugins: [],
}
