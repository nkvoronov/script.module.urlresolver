"""
    Plugin for UrlResolver
    Copyright (C) 2020 gujal

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

import re
from urlresolver import common
from urlresolver.plugins.lib import helpers
from urlresolver.resolver import UrlResolver, ResolverError


class AparatResolver(UrlResolver):
    name = "aparat"
    domains = ['aparat.cam']
    pattern = r'(?://|\.)(aparat\.cam)/(?:embed-)?([0-9a-zA-Z]+)'

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'Referer': web_url, 'User-Agent': common.FF_USER_AGENT}
        html = self.net.http_GET(web_url, headers=headers).content

        match = re.search(r'&hash=([^&]+)', html)
        if match:
            web_url = 'https://{0}/dl?op=download_orig&id={1}&mode=o&hash={2}'.format(host, media_id, match.group(1))
            html = self.net.http_GET(web_url, headers=headers).content
            r = re.search(r'<a\s*href="([^"]+)[^>]+>Direct', html)
            if r:
                return r.group(1) + helpers.append_headers({'User-Agent': common.FF_USER_AGENT})

        raise ResolverError('Video Link Not Found')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, 'https://{host}/embed-{media_id}.html')
