# -*- coding: utf-8 -*-
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.opensearch_store import OpenSearchOPDSStore
from calibre.gui2.store.search_result import SearchResult

class FlibustaStore(BasicStoreConfig, OpenSearchOPDSStore):

    name = 'Флибуста'
    open_search_url = 'https://flub.flibusta.is/opds/search'
    web_url = 'https://flibusta.is/'
    
    # Override to use the direct search URL from the OpenSearch description
    def get_opensearch_description_url(self):
        return None  # We'll use the direct search URL instead

    def search(self, query, max_results=10, timeout=60):
        # Use the direct search URL from flibusta.is
        from urllib.parse import quote_plus
        search_url = 'https://flub.flibusta.is/opds/search?searchTerm={}&searchType=books'.format(quote_plus(query))
        
        try:
            from calibre import browser
            from calibre.ebooks.metadata import MetaInformation
            
            br = browser()
            br.set_handle_robots(False)
            br.addheaders = [('User-Agent', 'Calibre')]
            
            response = br.open_novisit(search_url, timeout=timeout)
            raw_data = response.read()
            
            # Parse OPDS feed
            try:
                from lxml import etree
            except ImportError:
                import xml.etree.ElementTree as etree
            
            # Handle different encodings
            if isinstance(raw_data, bytes):
                try:
                    raw_data = raw_data.decode('utf-8')
                except UnicodeDecodeError:
                    raw_data = raw_data.decode('cp1251', errors='replace')
            
            root = etree.fromstring(raw_data.encode('utf-8') if isinstance(raw_data, str) else raw_data)
            
            # Define namespace
            ns = {'atom': 'http://www.w3.org/2005/Atom',
                  'dc': 'http://purl.org/dc/terms/',
                  'opds': 'http://opds-spec.org/2010/catalog'}
            
            count = 0
            for entry in root.xpath('//atom:entry', namespaces=ns):
                if count >= max_results:
                    break
                    
                s = SearchResult()
                
                # Extract title
                title_elem = entry.xpath('.//atom:title', namespaces=ns)
                s.title = title_elem[0].text.strip() if title_elem and title_elem[0].text else 'Unknown Title'
                
                # Extract author
                author_elem = entry.xpath('.//atom:author/atom:name', namespaces=ns)
                if not author_elem:
                    author_elem = entry.xpath('.//dc:creator', namespaces=ns)
                s.author = author_elem[0].text.strip() if author_elem and author_elem[0].text else 'Unknown Author'
                
                # Extract ID for constructing URLs
                id_elem = entry.xpath('.//atom:id', namespaces=ns)
                book_id = None
                if id_elem and id_elem[0].text:
                    # Extract numeric ID from the full ID
                    id_text = id_elem[0].text
                    import re
                    id_match = re.search(r'(\d+)', id_text)
                    if id_match:
                        book_id = id_match.group(1)
                
                # Extract links
                links = entry.xpath('.//atom:link', namespaces=ns)
                s.downloads = {}
                
                for link in links:
                    href = link.get('href')
                    rel = link.get('rel', '')
                    link_type = link.get('type', '')
                    title = link.get('title', '')
                    
                    if not href:
                        continue
                        
                    # Make URL absolute if relative
                    if href.startswith('/'):
                        href = 'https://flub.flibusta.is' + href
                    elif not href.startswith('http'):
                        href = 'https://flub.flibusta.is/' + href
                    
                    if rel == 'alternate' and ('html' in link_type or not link_type):
                        s.detail_item = href
                    elif 'acquisition' in rel or 'download' in rel.lower():
                        # Determine format from type or URL
                        format_name = None
                        if 'fb2' in link_type.lower() or 'fb2' in href.lower() or 'fb2' in title.lower():
                            format_name = 'FB2'
                        elif 'epub' in link_type.lower() or 'epub' in href.lower() or 'epub' in title.lower():
                            format_name = 'EPUB'
                        elif 'mobi' in link_type.lower() or 'mobi' in href.lower() or 'mobi' in title.lower():
                            format_name = 'MOBI'
                        elif 'pdf' in link_type.lower() or 'pdf' in href.lower() or 'pdf' in title.lower():
                            format_name = 'PDF'
                        elif 'txt' in link_type.lower() or 'txt' in href.lower() or 'txt' in title.lower():
                            format_name = 'TXT'
                        
                        if format_name:
                            s.downloads[format_name] = href
                
                # If no downloads found but we have book_id, construct download URLs
                if not s.downloads and book_id:
                    base_url = 'https://flub.flibusta.is/b/' + book_id
                    s.downloads['FB2'] = base_url + '/fb2'
                    s.downloads['EPUB'] = base_url + '/epub'
                    s.downloads['MOBI'] = base_url + '/mobi'
                
                # Set detail item if not found
                if not s.detail_item and book_id:
                    s.detail_item = 'https://flibusta.is/b/' + book_id
                
                # Extract summary/description
                summary_elem = entry.xpath('.//atom:summary', namespaces=ns)
                if not summary_elem:
                    summary_elem = entry.xpath('.//atom:content', namespaces=ns)
                
                if summary_elem and summary_elem[0].text:
                    s.comments = summary_elem[0].text.strip()
                
                # Extract publication date
                date_elem = entry.xpath('.//atom:published', namespaces=ns)
                if not date_elem:
                    date_elem = entry.xpath('.//atom:updated', namespaces=ns)
                if date_elem and date_elem[0].text:
                    try:
                        from datetime import datetime
                        date_str = date_elem[0].text
                        # Parse ISO format date
                        if 'T' in date_str:
                            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        else:
                            dt = datetime.strptime(date_str[:10], '%Y-%m-%d')
                        s.pubdate = dt
                    except:
                        pass
                
                s.price = '$0.00'
                s.drm = SearchResult.DRM_UNLOCKED
                s.store_name = 'Флибуста'
                
                # Only yield if we have at least title and author
                if s.title != 'Unknown Title' or s.author != 'Unknown Author':
                    count += 1
                    yield s
                
        except Exception as e:
            # Log error but don't raise to prevent plugin crash
            import traceback
            self.log.error('Error searching flibusta.is: %s\n%s' % (e, traceback.format_exc()))

    def get_details(self, search_result, timeout):
        search_result.drm = SearchResult.DRM_UNLOCKED
        
        # If downloads weren't populated during search, try to construct them
        if not search_result.downloads and search_result.detail_item:
            # Extract book ID from detail URL if possible
            try:
                book_id = search_result.detail_item.split('/')[-1]
                base_download_url = 'https://flub.flibusta.is/b/'
                search_result.downloads["FB2"] = base_download_url + book_id + "/fb2"
                search_result.downloads["EPUB"] = base_download_url + book_id + "/epub"
                search_result.downloads["MOBI"] = base_download_url + book_id + "/mobi"
            except:
                pass
        
        # Set available formats based on downloads
        formats = list(search_result.downloads.keys())
        search_result.formats = ", ".join(formats) if formats else "FB2, EPUB, MOBI"
        
        return True