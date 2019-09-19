"""
    URLResolver Kodi module
    Bitchute plugin
    Copyright (C) 2019 twilight0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __generic_resolver__ import UrlResolver
from lib import helpers
from urlresolver import common


class BitchuteResolver(UrlResolver):

    name = "bitchute.com"
    domains = ['bitchute.com']
    pattern = r'(?://|\.)(bitchute\.com)/(?:video|embed)/([\w-]+)/'

    def __init__(self):

        self.net = common.Net()

    def get_media_url(self, host, media_id):

        web_url = self.get_url(host, media_id)
        response = self.net.http_GET(web_url)

        sources = helpers.scrape_sources(
            response.content, patterns=[r'''source src=['"](?P<url>https.+?\.mp4)['"] type="video/mp4''']
        )

        return helpers.pick_source(sources)

    def get_url(self, host, media_id):

        return self._default_get_url(host, media_id, 'https://www.{host}/video/{media_id}')
