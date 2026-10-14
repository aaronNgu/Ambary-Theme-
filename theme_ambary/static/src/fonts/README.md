# bilo

The live site renders body copy, navigation, buttons and h3+ in **bilo**
(400 and 700), a licensed Latinotype face served from the WordPress child theme.

It is not bundled here yet. To wire it up:

1. Drop `bilo-400.woff2` and `bilo-700.woff2` in this directory.
2. Uncomment the `@font-face` pair in `../scss/fonts.scss`.
3. In `../scss/primary_variables.scss`, add to `$o-theme-font-configs`:
   `'Bilo': ('family': ('bilo', sans-serif))`  - no `'url'` key, which is how
   core declares `SYSTEM_FONTS` and what stops Odoo emitting a Google Fonts
   `@import`.
4. Change the six `-> 'Bilo'` marked values in the website values palette, and
   the four font keys in `models/theme_utils.py`.

Sources (both 200 OK at time of writing):
- https://storage.googleapis.com/ployai/4933a8b6-2378-46b6-89b4-3b3a9578b3b9/user/5b6205e9-bilo-400.woff2  (22.0 KB)
- https://storage.googleapis.com/ployai/4933a8b6-2378-46b6-89b4-3b3a9578b3b9/user/dfbeadc9-bilo-700.woff2  (22.6 KB)
- https://ambarygardens.com/wp-content/themes/Divi-child/fonts/bilo-{400,700}.woff  (older format)

The webfont licence may be scoped to ambarygardens.com; worth confirming before
serving it from another host.
