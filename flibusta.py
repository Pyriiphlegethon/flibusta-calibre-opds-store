# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = '2017, Anri Engelhardt <kriusmacht@gmail.com>'
__docformat__ = 'restructuredtext en'

from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.opensearch_store import OpenSearchOPDSStore
from calibre.gui2.store.search_result import SearchResult

class FlibustaStore(BasicStoreConfig, OpenSearchOPDSStore):

    open_search_url = 'http://flibusta.is/opds-opensearch.xml'
    web_url = 'http://flibusta.is/'

    def search(self, query, max_results=10, timeout=60):
        for s in OpenSearchOPDSStore.search(self, query, max_results, timeout):
            s.detail_item = 'http://flibusta.is/b/' + s.detail_item.split(':')[-1]
            s.price = '$0.00'
            s.drm = SearchResult.DRM_UNLOCKED
            yield s

    def get_details(self, search_result, timeout):
        search_result.drm = SearchResult.DRM_UNLOCKED
        search_result.formats = "FB2, EPUB, MOBI"
        search_result.downloads["FB2"] = search_result.detail_item + "/fb2"
        search_result.downloads["EPUB"] = search_result.detail_item + "/epub"
        search_result.downloads["MOBI"] = search_result.detail_item + "/mobi"
        return True