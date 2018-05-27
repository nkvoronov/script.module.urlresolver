"""
    OVERALL CREDIT TO:
        t0mm0, Eldorado, VOINAGE, BSTRDMKR, tknorris, smokdpi, TheHighway

    urlresolver XBMC Addon
    Copyright (C) 2011 t0mm0

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
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError
import re


class loadvidResolver(UrlResolver):
    name = "loadvid"
    domains = ['loadvid.online']
    pattern = '(?://|\.)(loadvid\.online)/embed/([\w-]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'en-US,en;q=0.9'}
        html = self.net.http_GET(web_url,headers=headers).content
        match=re.compile("/player\?(.+?)'").findall(html)[0]
        html = self.net.http_GET('https://loadvid.online/player?'+match,headers=headers).content

        source = re.compile('"src":"(.+?)"').findall(html.replace('\\n','').replace('\\',''))[0]
        host= source.split('//')[1]
        host= host.split('/')[0]
        EXTRA = '|Host=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36&Referer=%s' %(host,web_url)

        return source+EXTRA

        

        raise ResolverError('Unable to resolve kingfiles link. Filelink not found.')

    def get_url(self, host, media_id):
        return 'https://loadvid.online/embed/%s' % (media_id)
