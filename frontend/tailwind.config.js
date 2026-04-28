/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,ts}"],
  darkMode: ['selector', '[data-theme="dark"]'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['"Instrument Serif"', 'ui-serif', 'Georgia', 'serif'],
      },
      // Keep a small, meaningful palette. CSS variables stay the source of truth;
      // these keys let Tailwind utilities (e.g. `text-ink`, `bg-surface`) resolve.
      colors: {
        brand: {
          DEFAULT: '#740DC2',
          50:  '#FAF5FF',
          100: '#F4EEFB',
          200: '#E9D5FF',
          300: '#D8B4FE',
          400: '#A855F7',
          500: '#8B2BDB',
          600: '#740DC2',
          700: '#5B0A99',
          800: '#3D1766',
          900: '#2A1045',
        },
        ink: {
          DEFAULT: '#0A0908',
          soft: '#1C1917',
          muted: '#78716C',
        },
        surface: {
          DEFAULT: '#FFFFFF',
          subtle: '#FDFCFA',
          sunken: '#F5F3EF',
          canvas: '#FAFAF7',  // body background
        },
        line: {
          DEFAULT: '#E8E5DF',
          soft: '#F0EDE7',
        },
        sale: '#C2410C',
      },
      borderRadius: {
        sm: '10px',
        md: '14px',
        lg: '22px',
        xl: '28px',
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
      boxShadow: {
        soft: '0 1px 2px rgba(28,25,23,0.04)',
        lift: '0 6px 16px rgba(28,25,23,0.06), 0 24px 48px rgba(28,25,23,0.08)',
        glow: '0 10px 40px -10px rgba(116,13,194,0.35)',
      },
      transitionTimingFunction: {
        smooth: 'cubic-bezier(0.22, 1, 0.36, 1)',
        inout: 'cubic-bezier(0.76, 0, 0.24, 1)',
      },
      transitionDuration: {
        250: '250ms',
        500: '500ms',
        900: '900ms',
        1100: '1100ms',
      },
      animation: {
        'fade-in': 'fadeIn 900ms cubic-bezier(0.22,1,0.36,1) both',
        'slide-up': 'rise 1100ms cubic-bezier(0.22,1,0.36,1) both',
      },
      keyframes: {
        fadeIn: { '0%': { opacity: '0' }, '100%': { opacity: '1' } },
        rise: {
          '0%': { opacity: '0', transform: 'translateY(18px)', filter: 'blur(2px)' },
          '100%': { opacity: '1', transform: 'translateY(0)', filter: 'blur(0)' },
        },
      },
      maxWidth: {
        '7xl': '1280px',
      },
    },
  },
  plugins: [],
};
