# CSS architecture

The site uses a plain-CSS adaptation of Augmented ITCSS. `styles.css` is the
single entry point and imports layers from broad, low-specificity rules to
localized overrides:

1. `settings` — design tokens and theme values.
2. `generic` — resets and box sizing.
3. `elements` — bare HTML element defaults.
4. `building-blocks` — small reusable class-based controls.
5. `modules` — recognizable interface sections.
6. `frameworks` — page and grid composition.
7. `utilities` — single-purpose helpers.
8. `trumps` — accessibility, reduced-motion, and print overrides.

The Sass-oriented `tools` layer is intentionally omitted because this site has
no preprocessor. Class namespaces make ownership visible: `b-` for building
blocks, `m-` for modules, `f-` for frameworks, `u-` for utilities, and `t-`
for trumps. Components use flat BEM-style element and modifier names.
