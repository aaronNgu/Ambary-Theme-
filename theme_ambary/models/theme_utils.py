# -*- coding: utf-8 -*-
from odoo import api, models


class ThemeUtils(models.AbstractModel):
    _inherit = 'theme.utils'

    @api.model
    def _reset_default_config(self):
        """Disable Ambary's layout before Odoo restores its default variants.

        Theme removal resets the default configuration before unlinking the
        outgoing theme's views. Ambary's variants are not in Odoo's built-in
        template lists, so leaving them active conflicts with the default
        header/footer during that reset. disable_view only affects copies on
        the current website, including when another website keeps this theme.
        """
        self.disable_view('theme_ambary.template_header_ambary')
        self.disable_view('theme_ambary.template_footer_ambary')
        self.disable_view('theme_ambary.footer_copyright_ambary')
        return super()._reset_default_config()

    @api.model
    def _theme_ambary_post_copy(self, mod):
        """Pick the Ambary header/footer the first time the theme is applied.

        Called from ``ir.module.module._theme_load`` only when ``apply_new_theme``
        is in the context, i.e. on first install for a given website -- never on
        a later module upgrade, so it will not overwrite a choice the user made
        in the editor afterwards.
        """
        # theme.utils.enable_view() auto-disables the sibling variants only for
        # the xml_ids hardcoded in _header_templates / _footer_templates. Ours
        # are not in those lists, so clear Odoo's variants explicitly -- two
        # active header views would both xpath //header//nav and the second
        # would fail to locate its node.
        for view in self._header_templates:
            self.disable_view(view)
        for view in self._footer_templates:
            self.disable_view(view)

        self.enable_view('theme_ambary.template_header_ambary')
        self.enable_view('theme_ambary.template_footer_ambary')
        self.enable_view('theme_ambary.footer_copyright_ambary')

        # Design tokens. These land in the per-website user_values.scss map, so
        # they behave exactly as if a designer had picked them in the Theme tab
        # and stay editable there.
        self.env['web_editor.assets'].make_scss_customization(
            '/website/static/src/scss/options/user_values.scss',
            {
                'header-template': "'ambary'",
                'footer-template': "'ambary'",
                'color-palettes-name': "'ambary'",
                # Manrope stands in for bilo; see static/src/fonts/README.md.
                'font': "'Manrope'",
                'navbar-font': "'Manrope'",
                'buttons-font': "'Manrope'",
                'headings-font': "'Fraunces'",
            },
        )
