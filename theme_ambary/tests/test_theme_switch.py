from odoo.tests import TransactionCase, tagged
from odoo.addons.website.tools import MockRequest


@tagged('-at_install', 'post_install')
class TestAmbaryThemeSwitch(TransactionCase):
    """Exercise the removal path used by both theme switching and unselection."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.theme = cls.env['ir.module.module'].search(
            [('name', '=', 'theme_ambary')], limit=1,
        )
        cls.layout_keys = [
            'theme_ambary.template_header_ambary',
            'theme_ambary.template_footer_ambary',
            'theme_ambary.footer_copyright_ambary',
        ]

    def _new_website(self):
        return self.env['website'].create({'name': 'Ambary theme switch test'})

    def _apply_theme(self, website):
        website.theme_id = self.theme
        self.theme.with_context(
            website_id=website.id, apply_new_theme=True,
        )._theme_load(website)
        self.assertEqual(len(self._active_layout_views(website)), 3)

    def _active_layout_views(self, website):
        return self.env['ir.ui.view'].search([
            ('website_id', '=', website.id),
            ('key', 'in', self.layout_keys),
        ])

    def _assert_default_layout(self, website):
        website = website.with_context(website_id=website.id)
        self.assertTrue(website.viewref('website.template_header_default').active)
        self.assertTrue(website.viewref('website.footer_custom').active)
        self.assertFalse(self._active_layout_views(website))

    def test_remove_and_reapply_theme(self):
        website = self._new_website()
        self._apply_theme(website)

        # This previously raised "//header//nav cannot be located" while
        # enabling the default header, before Ambary's views were unlinked.
        modules = self.env['ir.module.module'].with_context(website_id=website.id)
        modules._theme_remove(website)
        self.assertFalse(website.theme_id)
        self._assert_default_layout(website)

        self._apply_theme(website)
        modules._theme_remove(website)
        self._assert_default_layout(website)

    def test_remove_does_not_change_another_website(self):
        first = self._new_website()
        second = self._new_website()
        self._apply_theme(first)
        self._apply_theme(second)

        self.env['ir.module.module'].with_context(
            website_id=first.id,
        )._theme_remove(first)

        self._assert_default_layout(first)
        self.assertEqual(second.theme_id, self.theme)
        self.assertEqual(len(self._active_layout_views(second)), 3)
        self.assertFalse(second.with_context(website_id=second.id).viewref(
            'website.template_header_default',
        ).active)

    def test_reset_without_ambary_copies(self):
        website = self._new_website()
        self.env['theme.utils'].with_context(
            website_id=website.id,
        )._reset_default_config()
        self._assert_default_layout(website)

    def _render_product_cards(self, website, template_key, product):
        product_filter = self.env.ref(
            'website_sale.dynamic_filter_newest_products',
        ).with_context(website_id=website.id)
        with MockRequest(product_filter.env, website=website.with_env(product_filter.env)):
            return product_filter._render(
                template_key, limit=1, search_domain=[('id', '=', product.id)],
            )

    def _new_product(self):
        return self.env['product.product'].create({
            'name': 'Theme switch test product',
            'website_published': True,
            'list_price': 10,
        })

    def test_product_cards_survive_removal_and_reapply(self):
        website = self._new_website()
        product = self._new_product()
        ambary_key = 'theme_ambary.dynamic_filter_template_product_product_ambary'
        default_key = 'website_sale.dynamic_filter_template_product_product_view_detail'
        self._apply_theme(website)
        cards = self._render_product_cards(website, ambary_key, product)
        self.assertEqual(len(cards), 1)
        self.assertIn('o_ambary_product_card', cards[0])

        self.env['ir.module.module'].with_context(
            website_id=website.id,
        )._theme_remove(website)
        cards = self._render_product_cards(website, ambary_key, product)
        self.assertEqual(len(cards), 1)
        self.assertIn(product.name, cards[0])
        self.assertNotIn('o_ambary_product_card', cards[0])
        self.assertEqual(cards, self._render_product_cards(website, default_key, product))

        self._apply_theme(website)
        cards = self._render_product_cards(website, ambary_key, product)
        self.assertIn('o_ambary_product_card', cards[0])

    def test_product_fallback_is_website_specific(self):
        first = self._new_website()
        second = self._new_website()
        product = self._new_product()
        key = 'theme_ambary.dynamic_filter_template_product_product_ambary'
        self._apply_theme(first)
        self._apply_theme(second)
        self.env['ir.module.module'].with_context(
            website_id=first.id,
        )._theme_remove(first)

        first_cards = self._render_product_cards(first, key, product)
        second_cards = self._render_product_cards(second, key, product)
        self.assertEqual(len(first_cards), 1)
        self.assertEqual(len(second_cards), 1)
        self.assertNotIn('o_ambary_product_card', first_cards[0])
        self.assertIn('o_ambary_product_card', second_cards[0])

    def test_unrelated_missing_product_templates_still_raise(self):
        website = self._new_website()
        with self.assertRaises(ValueError):
            self._render_product_cards(
                website, 'other_theme.dynamic_filter_template_product_product_missing',
                self._new_product(),
            )
