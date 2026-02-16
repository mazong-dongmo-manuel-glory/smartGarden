/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'sans-serif']
            },
            colors: {
                primary: '#10b981',
                secondary: '#059669',
                dark: '#1f2937',
                danger: '#ef4444',
                warning: '#f59e0b'
            }
        },
    },
    plugins: [],
}
