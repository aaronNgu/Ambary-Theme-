# -*- coding: utf-8 -*-
"""Repair footer logos saved as raw base64 text by the website editor."""
import logging

from lxml import etree

from odoo import SUPERUSER_ID, api


_logger = logging.getLogger(__name__)


def _replace_logo_contents(arch):
    root = etree.fromstring(arch.encode())
    anchors = root.xpath(
        ".//a[contains(concat(' ', normalize-space(@class), ' '), "
        "' o_ambary_footer_logo ')]"
    )
    if not anchors:
        return arch, False

    changed = False
    for anchor in anchors:
        children = list(anchor)
        already_safe = (
            len(children) == 1
            and children[0].tag == 'img'
            and children[0].get('t-att-src')
            == "'/web/image/website/%s/logo' % website.id"
            and not (anchor.text or '').strip()
        )
        if already_safe:
            continue

        anchor.text = None
        for child in children:
            anchor.remove(child)
        etree.SubElement(anchor, 'img', {
            't-att-src': "'/web/image/website/%s/logo' % website.id",
            'class': 'img-fluid',
            'width': '190',
            'height': '80',
            'role': 'img',
            't-att-alt': "'Logo of %s' % website.name",
            't-att-title': 'website.name',
        })
        changed = True

    return etree.tostring(root, encoding='unicode'), changed


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    module = env['ir.module.module'].search([('name', '=', 'theme_ambary')], limit=1)
    if not module:
        return

    for website in module._theme_get_stream_website_ids():
        _logger.info("theme_ambary: copying updated templates to website %s", website.id)
        module._theme_load(website)

    footer_views = env['ir.ui.view'].with_context(active_test=False).search([
        ('key', '=', 'theme_ambary.template_footer_ambary'),
        ('website_id', '!=', False),
    ])
    for view in footer_views:
        repaired_arch, changed = _replace_logo_contents(view.arch_db)
        if changed:
            _logger.info("theme_ambary: repairing footer logo in view %s", view.id)
            view.arch_db = repaired_arch
