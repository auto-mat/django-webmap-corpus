# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WebmapConfig(AppConfig):
    name = 'webmap'
    verbose_name = _("Webmap")
