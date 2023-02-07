"""
    plugin for URLResolver
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
import random
import string
import time
from urlresolver.plugins.lib import helpers
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError


class DoodStreamResolver(UrlResolver):
    name = "doodstream"
    domains = ['dood.watch', 'doodstream.com', 'dood.to', 'dood.so', 'dood.cx', 'dood.la', 'dood.ws', 'dood.pm']
    pattern = r'(?://|\.)(dood(?:stream)?\.(?:com|watch|to|so|cx|la|ws|pm))/(?:d|e)/([0-9a-zA-Z]+)'

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        common.log('DoodStreamResolver.get_media_url')
        headers = {'User-Agent': common.RAND_UA,
                   'Referer': 'https://{0}/'.format(host)}

        r = self.net.http_GET(web_url, headers=headers)
        common.log(r.get_url())
        if r.get_url() != web_url:
            common.log('r.get_url() != web_url')
            host = re.findall(r'(?://|\.)([^/]+)', r.get_url())[0]
            common.log(host)
            web_url = self.get_url(host, media_id)
            common.log(web_url)
        headers.update({'Referer': web_url})

        html = r.content
        match = re.search(r'''dsplayer\.hotkeys[^']+'([^']+).+?function\s*makePlay.+?return[^?]+([^"]+)''', html, re.DOTALL)
        if match:
            common.log('match')
            token = match.group(2)
            common.log(token)
            url = 'https://{0}{1}'.format(host, match.group(1))
            common.log(url)
            html = self.net.http_GET(url, headers=headers).content
            common.log(html)
            common.log(str(int(time.time() * 1000)))
            return self.dood_decode(html) + token + str(int(time.time() * 1000)) + helpers.append_headers(headers)

        raise ResolverError('Video Link Not Found')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/e/{media_id}')

    def dood_decode(self, data):
        common.log('DoodStreamResolver.dood_decode')
        t = string.ascii_letters + string.digits
        common.log(t)
        s = ''.join([random.choice(t) for _ in range(10)])
        common.log(s)
        return data + ''.join([random.choice(t) for _ in range(10)])
