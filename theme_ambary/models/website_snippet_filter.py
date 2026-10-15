from odoo import models


class WebsiteSnippetFilter(models.Model):
    _inherit = 'website.snippet.filter'

    def _render(self, template_key, limit, search_domain=None, with_sample=False,
                **custom_template_data):
        # Saved Products blocks keep their template key when a theme is removed,
        # but Odoo deletes that theme's website-specific template copies. Keep
        # these blocks usable without rewriting the user's saved page content.
        if template_key == 'theme_ambary.dynamic_filter_template_product_product_ambary':
            website = self.env['website'].get_current_website()
            website = website.with_context(website_id=website.id)
            if not website.viewref(template_key, raise_if_not_found=False):
                template_key = 'website_sale.dynamic_filter_template_product_product_view_detail'

        return super()._render(
            template_key, limit, search_domain=search_domain,
            with_sample=with_sample, **custom_template_data,
        )
