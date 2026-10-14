# -*- coding: utf-8 -*-
"""Copy updated theme templates to every website already using the theme.

Theme XML is stored first as ``theme.ir.ui.view`` records. Odoo must then copy
those templates to website-specific ``ir.ui.view`` records before the snippet
registry can render them. Force that copy here so newly added snippets are
available on websites where the theme was already installed.
"""
import logging

from odoo import SUPERUSER_ID, api


_logger = logging.getLogger(__name__)


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
