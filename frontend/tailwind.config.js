/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        'pro-blue': '#1e3a8a',
        'pro-gray': '#4a5568',
      },
    },
  },
  plugins: [],
};