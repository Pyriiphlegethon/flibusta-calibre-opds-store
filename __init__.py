# -*- coding: utf-8 -*-

#copyright Pyriiphlegethon 2025 
from calibre.customize import StoreBase

# Localization function - will be provided by Calibre at runtime
def _(text):
    return text

class FlibustaStore(StoreBase):
    name = 'Флибуста'
    description = _('Книжное братство - flibusta.is')
    actual_plugin = 'calibre_plugins.store_flibusta.flibusta:FlibustaStore'
    author = 'Anri Engelhardt'
    version = (1, 1, 0)
    minimum_calibre_version = (3, 0, 0)

    drm_free_only = True
    headquarters = 'RU'
    formats = ['EPUB', 'TXT', 'RTF', 'HTML', 'FB2', 'PDF', 'MOBI']
    affiliate = False
