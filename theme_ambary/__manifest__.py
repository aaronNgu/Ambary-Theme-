# -*- coding: utf-8 -*-
{
    'name': "Ambary Gardens Theme",
    'summary': "Brand header, footer and design tokens for Ambary Gardens",
    'author': "Aaron Ngu",
    'category': 'Theme/Creative',
    'version': '18.0.1.0.10',
    'license': 'LGPL-3',
    # website_sale is a hard dependency because the header renders the cart.
    # Split this into theme_ambary + theme_ambary_sale if the theme ever has to
    # run on a non-eCommerce site.
    'depends': ['website', 'website_sale'],
    'data': [
        'views/header.xml',
        'views/footer.xml',
        'views/snippets/s_ambary_hero.xml',
        'views/snippets/s_ambary_intro.xml',
        'views/snippets/s_ambary_experience.xml',
        'views/snippets/s_ambary_categories.xml',
        'views/snippets/s_ambary_effects.xml',
        'views/snippets/dynamic_filter_template_product_product_ambary.xml',
        'views/snippets.xml',
        'views/snippet_options.xml',
    ],
    'assets': {
        # NOTE: appended, not prepended. website/.../primary_variables.scss
        # declares its values with !default, so a *later* plain assignment wins.
        # Prepending would put this file ahead of web_editor.variables.scss and
        # $o-color-palettes / o-make-palette() would not exist yet.
        'web._assets_primary_variables': [
            'theme_ambary/static/src/scss/primary_variables.scss',
        ],
        'web._assets_secondary_variables': [
            'theme_ambary/static/src/scss/secondary_variables.scss',
        ],
        # Prepended so it beats bootstrap/_variables.scss to the !default.
        'web._assets_frontend_helpers': [
            ('prepend', 'theme_ambary/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            'theme_ambary/static/src/scss/fonts.scss',
            'theme_ambary/static/src/scss/theme.scss',
        ],
    },
}
