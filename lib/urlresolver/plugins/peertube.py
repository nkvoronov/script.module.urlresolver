"""
    Plugin for URLResolver
    Copyright (C) 2021 gujal

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

import json
from urlresolver.plugins.lib import helpers
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError


class PeerTubeResolver(UrlResolver):
    name = "peertube"
    domains = ["peertube.uno"]
    pattern = r'(?://|\.)(peertube\.uno)/videos/(?:embed|watch)/([0-9a-f-]+)'

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.FF_USER_AGENT,
                   'Referer': 'https://{0}/'.format(host)}
        html = self.net.http_GET(web_url, headers).content
        item = json.loads(html).get('streamingPlaylists')
        if item:
            return item[0].get('playlistUrl') + helpers.append_headers(headers)

        raise ResolverError('File Not Found or removed')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/api/v1/videos/{media_id}')
