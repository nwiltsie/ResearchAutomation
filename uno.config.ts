import { defineConfig } from 'unocss'

export default defineConfig({
  rules: [
    ['th-bold', { 'font-weight': 'bold !important' }],
  ],
  preflights: [
    {
      getCSS: () => `
        .slidev-layout th {
          @apply th-bold;
        }
      `,
    },
  ],
})
