/**
 * Tailwind CSS Configuration for uu_framework
 * Uses CSS custom properties for theming
 */

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./uu_framework/eleventy/_includes/**/*.{njk,html}",
    "./clase/**/*.md",
    "./_site/**/*.html",
    // Safelist commonly used classes that might not be detected
  ],
  safelist: [
    // Backgrounds
    'bg-bg', 'bg-bg-secondary', 'bg-bg-tertiary', 'bg-code-bg', 'bg-accent',
    'bg-bg-secondary/95',
    // Text colors
    'text-text', 'text-text-muted', 'text-accent', 'text-accent-secondary', 'text-bg',
    'text-accent-hover', 'text-homework', 'text-exercise', 'text-prompt', 'text-example', 'text-exam',
    'text-calendar-class', 'text-calendar-holiday',
    // Borders
    'border-border', 'border-l-2', 'border-l-4',
    'border-homework', 'border-exercise', 'border-exam', 'border-project',
    'border-calendar-class', 'border-calendar-holiday',
    // Hovers
    'hover:text-accent', 'hover:text-accent-hover', 'hover:text-text',
    'hover:bg-bg-secondary', 'hover:bg-bg-tertiary', 'hover:scale-110',
    // Layout
    'min-h-screen', 'antialiased', 'font-sans', 'font-mono',
    'flex', 'flex-col', 'flex-row', 'flex-1', 'flex-shrink-0', 'flex-wrap',
    'items-center', 'items-start', 'justify-between', 'justify-end',
    'space-x-1', 'space-x-2', 'space-x-3', 'space-x-6',
    'space-y-0.5', 'space-y-1', 'space-y-2', 'space-y-4',
    'gap-2', 'gap-4', 'gap-8',
    // Spacing
    'p-2', 'p-3', 'p-4',
    'px-2', 'px-3', 'px-4', 'py-1', 'py-1.5', 'py-2', 'py-2.5', 'py-6', 'py-8',
    'mx-1', 'mx-2', 'mx-auto',
    'mb-2', 'mb-3', 'mb-4', 'mb-6', 'mb-8',
    'mt-1', 'mt-2', 'mt-3', 'mt-8', 'mt-12', 'mt-16', 'mt-auto',
    'mr-2', 'mr-2.5', 'mr-3', 'ml-2', 'ml-4', 'ml-6', 'pl-3', 'pt-6', 'pt-8',
    // Sizing
    'w-full', 'w-4', 'w-5', 'w-6', 'w-1.5',
    'h-5', 'h-6', 'h-14', 'h-16', 'h-1.5',
    'max-w-7xl', 'max-w-none',
    // Typography
    'text-xs', 'text-sm', 'text-lg', 'text-xl', 'text-2xl', 'text-3xl', 'text-4xl',
    'font-bold', 'font-medium',
    'uppercase', 'tracking-wide', 'tracking-wider',
    'text-center', 'text-right',
    // Borders & Radius
    'rounded', 'rounded-lg', 'rounded-full',
    'border-b', 'border-l', 'border-t',
    // Positioning
    'sticky', 'top-0', 'z-40', 'z-50', 'relative', 'absolute', 'fixed',
    'right-2', 'top-2',
    // Display
    'hidden', 'block', 'inline-block',
    'md:flex', 'lg:flex-row', 'lg:w-56', 'lg:w-64',
    'lg:sticky', 'lg:top-20',
    'sm:flex-row', 'sm:justify-between', 'sm:items-start', 'sm:items-end',
    'sm:px-6', 'lg:px-8', 'sm:text-3xl', 'sm:text-4xl', 'sm:inline',
    // Effects
    'truncate', 'overflow-x-auto', 'whitespace-pre-wrap',
    'transition-colors', 'transition-all', 'transition-transform',
    'backdrop-blur',
    'group', 'group-hover:text-accent', 'group-hover:bg-accent', 'group-hover:scale-110',
    // Prose
    'prose', 'prose-lg',
    // Accessibility
    'sr-only', 'focus:not-sr-only', 'focus:absolute', 'focus:top-4', 'focus:left-4',
    // Additional layout
    'inset-0', 'left-0', 'h-screen', 'w-64', 'ml-64', 'overflow-y-auto',
    '-ml-2', 'mr-1', 'ml-5', 'mt-0.5', 'mb-1', 'pl-3', 'pr-2', 'py-4',
    'w-3', 'h-3', 'w-4', 'h-4', 'w-5',
    'rounded-r', 'grid', 'grid-cols-2',
    'transform', 'lg:text-3xl', 'lg:p-8',
    'bg-black/50', 'bg-bg/95',
    'p-1.5', 'h-12', 'mt-10', 'lg:p-6',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Theme colors using CSS variables
        'bg': 'var(--color-bg)',
        'bg-secondary': 'var(--color-bg-secondary)',
        'bg-tertiary': 'var(--color-bg-tertiary)',
        'text': 'var(--color-text)',
        'text-muted': 'var(--color-text-muted)',
        'accent': 'var(--color-accent)',
        'accent-hover': 'var(--color-accent-hover)',
        'accent-secondary': 'var(--color-accent-secondary)',
        'border': 'var(--color-border)',
        'code-bg': 'var(--color-code-bg)',
        // Component colors
        'homework': 'var(--color-homework)',
        'exercise': 'var(--color-exercise)',
        'prompt': 'var(--color-prompt)',
        'example': 'var(--color-example)',
        'exam': 'var(--color-exam)',
        'project': 'var(--color-project)',
        // Calendar colors
        'calendar-class': 'var(--color-calendar-class)',
        'calendar-holiday': 'var(--color-calendar-holiday)',
        'calendar-shadow': 'var(--color-calendar-shadow)',
      },
      fontFamily: {
        'sans': ['var(--font-family-base)'],
        'mono': ['var(--font-family-mono)'],
        'dyslexic': ['OpenDyslexic', 'sans-serif'],
      },
      typography: {
        DEFAULT: {
          css: {
            color: 'var(--color-text)',
            a: {
              color: 'var(--color-accent)',
              '&:hover': {
                color: 'var(--color-accent-hover)',
              },
            },
            code: {
              color: 'var(--color-text)',
              backgroundColor: 'var(--color-code-bg)',
            },
            'code::before': {
              content: '""',
            },
            'code::after': {
              content: '""',
            },
          },
        },
      },
    },
  },
  plugins: [],
}
