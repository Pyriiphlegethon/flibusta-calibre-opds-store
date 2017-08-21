# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = '2017, Anri Engelhardt <kriusmacht at gmail.com>'
__docformat__ = 'restructuredtext en'

from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.opensearch_store import OpenSearchOPDSStore
from calibre.gui2.store.search_result import SearchResult


class FlibustaStore(BasicStoreConfig, OpenSearchOPDSStore):

    open_search_url = 'http://flibusta.lib/opds-opensearch.xml'
    web_url = 'http://flibusta.lib/'

    def search(self, query, max_results=10, timeout=60):
        for s in OpenSearchOPDSStore.search(self, query, max_results, timeout):
            s.detail_item = 'http://flibusta.lib' + s.detail_item.split(':')[-1]
            s.price = '$0.00'
            s.drm = SearchResult.DRM_UNLOCKED
            s.formats = 'FB2, EPUB, MOBI'
            s.downloads["FB2"] = s.detail_item+"/fb2"
            s.downloads["EPUB"] = s.detail_item + "/epub"
            s.downloads["MOBI"] = s.detail_item + "/mobi"
            yield s