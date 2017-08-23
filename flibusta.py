# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = '2017, Anri Engelhardt <kriusmacht at gmail.com>'
__docformat__ = 'restructuredtext en'

from contextlib import closing

from lxml import etree

from PyQt5.Qt import QUrl

from calibre import (browser, guess_extension)
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.search_result import SearchResult
from calibre.utils.opensearch.description import Description
from calibre.utils.opensearch.query import Query


def open_search(url, query, max_results=10, timeout=60):
    url_template = 'http://flibusta.lib/opds/opensearch?searchTerm={searchTerms}&searchType=books&pageNumber={startPage?}'
    if not url_template:
        return
    oquery = Query(url_template)

    # set up initial values
    oquery.searchTerms = query
    oquery.count = max_results
    url = oquery.url()

    counter = max_results
    br = browser()
    with closing(br.open(url, timeout=timeout)) as f:
        doc = etree.fromstring(f.read())
        for data in doc.xpath('//*[local-name() = "entry"]'):
            if counter <= 0:
                break

            counter -= 1

            s = SearchResult()

            s.detail_item = ''.join(data.xpath('./*[local-name() = "id"]/text()')).strip()

            for link in data.xpath('./*[local-name() = "link"]'):
                rel = link.get('rel')
                href = link.get('href')
                type = link.get('type')

                if rel and href and type:
                    if 'http://opds-spec.org/thumbnail' in rel:
                        s.cover_url = href
                    elif 'http://opds-spec.org/image/thumbnail' in rel:
                        s.cover_url = href
                    elif 'http://opds-spec.org/acquisition/buy' in rel:
                        s.detail_item = href
                    elif 'http://opds-spec.org/acquisition/sample' in rel:
                        pass
                    elif 'http://opds-spec.org/acquisition' in rel:
                        if type:
                            ext = guess_extension(type)
                            if ext:
                                ext = ext[1:].upper().strip()
                                s.downloads[ext] = href
            s.formats = ', '.join(s.downloads.keys()).strip()

            s.title = ' '.join(data.xpath('./*[local-name() = "title"]//text()')).strip()
            s.author = ', '.join(data.xpath('./*[local-name() = "author"]//*[local-name() = "name"]//text()')).strip()

            price_e = data.xpath('.//*[local-name() = "price"][1]')
            if price_e:
                price_e = price_e[0]
                currency_code = price_e.get('currencycode', '')
                price = ''.join(price_e.xpath('.//text()')).strip()
                s.price = currency_code + ' ' + price
                s.price = s.price.strip()

            yield s


class OpenSearchOPDSStoreFlibusta(StorePlugin):

    open_search_url = ''
    web_url = ''

    def open(self, parent=None, detail_item=None, external=False):
        if not hasattr(self, 'web_url'):
            return

        if external or self.config.get('open_external', False):
            open_url(QUrl(detail_item if detail_item else self.web_url))
        else:
            d = WebStoreDialog(self.gui, self.web_url, parent, detail_item, create_browser=self.create_browser)
            d.setWindowTitle(self.name)
            d.set_tags(self.config.get('tags', ''))
            d.exec_()

    def search_open(self, query, max_results=10, timeout=60):
        if not getattr(self, 'open_search_url', None):
            return
        for result in open_search(self.open_search_url, query, max_results=max_results, timeout=timeout):
            yield result


class FlibustaStore(BasicStoreConfig, OpenSearchOPDSStoreFlibusta):

    open_search_url = 'http://flibusta.lib/opds-opensearch.xml'
    web_url = 'http://flibusta.lib/'

    def search(self, query, max_results=10, timeout=60):
        for s in OpenSearchOPDSStore.search_open(self, query, max_results, timeout):
            s.detail_item = 'http://flibusta.lib/b/' + s.detail_item.split(':')[-1]
            s.price = '$0.00'
            s.drm = SearchResult.DRM_UNLOCKED
            s.formats = 'FB2, EPUB, MOBI'
            s.downloads["FB2"] = s.detail_item+"/fb2"
            s.downloads["EPUB"] = s.detail_item + "/epub"
            s.downloads["MOBI"] = s.detail_item + "/mobi"
            yield s
