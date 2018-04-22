"""
    Copyright (C) 2017 tknorris

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
import os, thevid_gmu,re
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError
from lib import jsunpack

logger = common.log_utils.Logger.get_logger(__name__)
logger.disable()
VID_SOURCE = 'https://raw.githubusercontent.com/tvaddonsco/script.module.urlresolver/master/lib/urlresolver/plugins/thevid_gmu.py'
VID_PATH = os.path.join(common.plugins_path, 'thevid_gmu.py')

class TheVidResolver(UrlResolver):
    name = "TheVid"
    domains = ["thevid.net"]
    pattern = '(?://|\.)(thevid\.net)/(?:video|e|v)/([A-Za-z0-9]+)'
    
    def __init__(self):
        self.net = common.Net()
    
    def get_media_url(self, host, media_id):

        web_url = self.get_url(host, media_id)
        html = self.net.http_GET(web_url).content
        match=re.compile('<script>(.+?)</script>',re.DOTALL).findall(html)
        
        for source in match:
            source =source.strip()
            try:

                UNPACKED = jsunpack.unpack(source)
                if 'sfilea' in UNPACKED:
                    FINAL_URL = re.compile('sfilea="(.+?)"').findall(UNPACKED)[0]
                    if not 'http' in FINAL_URL:
                        FINAL_URL = 'http:'+ FINAL_URL
                    return FINAL_URL
            except:pass

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='http://{host}/e/{media_id}/')
        
    @classmethod
    def get_settings_xml(cls):
        xml = super(cls, cls).get_settings_xml()
        xml.append('<setting id="%s_auto_update" type="bool" label="Automatically update resolver" default="true"/>' % (cls.__name__))
        xml.append('<setting id="%s_etag" type="text" default="" visible="false"/>' % (cls.__name__))
        return xml
