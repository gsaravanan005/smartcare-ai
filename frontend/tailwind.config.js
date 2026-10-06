/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
      },
      colors: {
        darkBg: {
          base: '#080512',
          surface: '#0D0718',
          card: '#120A24',
          border: '#2A1A4E',
          glass: 'rgba(18, 10, 36, 0.75)'
        },
        purplePrimary: {
          DEFAULT: '#7C3AED',
          dark: '#6D28D9',
          bright: '#8B5CF6',
          light: '#A855F7'
        },
        neonAccent: {
          DEFAULT: '#C084FC',
          pink: '#E879F9',
          soft: '#D8B4FE'
        },
        typography: {
          primary: '#FFFFFF',
          secondary: '#E5E7EB',
          muted: '#A1A1AA'
        },
        statusSuccess: '#22C55E',
        statusWarning: '#F59E0B',
        statusDanger: '#EF4444'
      }
    },
  },
  plugins: [],
}
