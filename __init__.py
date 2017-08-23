# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = '2017, Anri Engelhardt <kriusmacht at gmail.com>'
__docformat__ = 'restructuredtext en'

from calibre.customize import StoreBase

class FlibustaStore(StoreBase):
    name = 'Флибуста'
    description = _('Книжное братство')
    actual_plugin = 'calibre_plugins.store_flibusta.flibusta:FlibustaStore'
    author = 'Anri Engelhardt'

    drm_free_only = True
    headquarters = 'RU'
    formats = ['EPUB', 'TXT', 'RTF', 'HTML', 'FB2', 'PDF', 'MOBI']
    affiliate = False
