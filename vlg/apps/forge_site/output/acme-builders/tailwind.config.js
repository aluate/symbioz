/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#5D7586',
        'secondary': '#F4F2EC',
        'background': '#F4F2EC',
        'text': '#2F3136',
        'accent': '#5D7586',
        
        'steel-blue': '#5D7586',
        'porcelain': '#F4F2EC',
        'graphite': '#2F3136',
        'lavender-gray': '#D9DCE0',
        
      },
      fontFamily: {
        sans: ["Inter","system-ui","-apple-system","sans-serif"],
      },
    },
  },
  plugins: [],
};
