# -*- coding: utf-8 -*-
"""Refresh the Why Ambary block in the picker without overwriting saved pages."""
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
