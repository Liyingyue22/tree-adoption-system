/** @type {import('tailwindcss').Config} */

export default {
  darkMode: 'class',
  content: ['./index.html', './admin.html', './src/**/*.{js,ts,vue}'],
  theme: {
    container: {
      center: true,
    },
    extend: {
      colors: {
        forest: {
          DEFAULT: '#1f4d2e',
          deep: '#163a22',
        },
        leaf: {
          DEFAULT: '#5b9d3c',
          light: '#8bc34a',
        },
        clay: {
          DEFAULT: '#d97a3d',
          deep: '#b85e25',
        },
        cream: {
          DEFAULT: '#f7f3ec',
          dark: '#efe8d8',
        },
        wood: '#7a5b3a',
        ink: '#2a2520',
      },
      fontFamily: {
        serif: ['Noto Serif SC', 'Source Han Serif SC', 'serif'],
        sans: ['HarmonyOS Sans SC', 'Noto Sans SC', 'PingFang SC', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      boxShadow: {
        soft: '0 4px 16px rgba(31, 77, 46, 0.08)',
        card: '0 8px 28px rgba(31, 77, 46, 0.12)',
        hover: '0 14px 38px rgba(31, 77, 46, 0.18)',
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false, // 避免 Tailwind reset 与 Element Plus 冲突
  },
}
