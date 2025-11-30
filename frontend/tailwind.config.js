/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#2563EB',
          600: '#1d4ed8',
          700: '#1e40af',
        },
        edu: {
          primary: '#2563EB',
          secondary: '#7C3AED',
          success: '#059669',
          warning: '#D97706',
          error: '#DC2626',
          teal: '#0891B2',
          indigo: '#4F46E5',
          pink: '#EC4899',
          forest: '#166534',
          amber: '#F59E0B',
        },
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        border: 'hsl(var(--border))',
      },
      backdropBlur: {
        xs: '2px',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'glass-morph': 'glassMorph 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        glassMorph: {
          '0%': { backdropFilter: 'blur(0px)', backgroundColor: 'rgba(255, 255, 255, 0)' },
          '100%': { backdropFilter: 'blur(16px)', backgroundColor: 'rgba(255, 255, 255, 0.2)' },
        },
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [
    function({ addUtilities }) {
      const newUtilities = {
        '.glass': {
          'backdrop-filter': 'blur(24px) saturate(180%)',
          '-webkit-backdrop-filter': 'blur(24px) saturate(180%)',
          'background-color': 'rgba(255, 255, 255, 0.85)',
          'border': '1px solid rgba(37, 99, 235, 0.2)',
          'color': '#0F172A',
        },
        '.dark .glass': {
          'background-color': 'rgba(15, 23, 42, 0.85)',
          'border': '1px solid rgba(124, 58, 237, 0.3)',
          'color': '#F8FAFC',
        },
        '.glass-strong': {
          'backdrop-filter': 'blur(24px) saturate(180%)',
          '-webkit-backdrop-filter': 'blur(24px) saturate(180%)',
          'background-color': 'rgba(255, 255, 255, 0.95)',
          'border': '1px solid rgba(37, 99, 235, 0.3)',
          'color': '#0F172A',
        },
        '.dark .glass-strong': {
          'background-color': 'rgba(15, 23, 42, 0.95)',
          'border': '1px solid rgba(124, 58, 237, 0.4)',
          'color': '#F8FAFC',
        },
        '.glass-nav': {
          'backdrop-filter': 'blur(32px) saturate(180%)',
          '-webkit-backdrop-filter': 'blur(32px) saturate(180%)',
          'background-color': 'rgba(255, 255, 255, 0.92)',
          'border-bottom': '2px solid rgba(37, 99, 235, 0.2)',
          'color': '#0F172A',
        },
        '.dark .glass-nav': {
          'background-color': 'rgba(15, 23, 42, 0.92)',
          'border-bottom': '2px solid rgba(124, 58, 237, 0.3)',
          'color': '#F8FAFC',
        },
        '.text-visible': {
          'color': '#0F172A !important',
          'font-weight': '600',
        },
        '.dark .text-visible': {
          'color': '#F8FAFC !important',
          'font-weight': '600',
        },
        '.bg-edu-gradient': {
          'background': 'linear-gradient(135deg, rgba(219, 234, 254, 0.6) 0%, rgba(233, 213, 255, 0.6) 20%, rgba(209, 250, 229, 0.6) 40%, rgba(254, 243, 199, 0.6) 60%, rgba(252, 231, 243, 0.6) 80%, rgba(219, 234, 254, 0.6) 100%)',
        },
        '.dark .bg-edu-gradient': {
          'background': 'linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(55, 48, 163, 0.8) 20%, rgba(6, 78, 59, 0.8) 40%, rgba(120, 53, 15, 0.8) 60%, rgba(131, 24, 67, 0.8) 80%, rgba(30, 41, 59, 0.8) 100%)',
        },
      }
      addUtilities(newUtilities)
    }
  ],
}