"""
    Kodi urlresolver plugin
    Copyright (C) 2014  smokdpi
    Updated by Gujal (c) 2016

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
import os
import fx_gmu
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError  # @UnusedImport

logger = common.log_utils.Logger.get_logger(__name__)
logger.disable()
FX_SOURCE = 'https://offshoregit.com/tvaresolvers/fx_gmu.py'
FX_PATH = os.path.join(common.plugins_path, 'fx_gmu.py')

class FlashxResolver(UrlResolver):
    name = "flashx"
    domains = ["flashx.tv"]
    pattern = '(?://|\.)(flashx\.tv)/(?:embed-|dl\?|embed.php\?c=)?([0-9a-zA-Z/-]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        try:
            self._auto_update(FX_SOURCE, FX_PATH)
            reload(fx_gmu)
            web_url = self.get_url(host, media_id)
            return fx_gmu.get_media_url(web_url)
        except Exception as e:
            logger.log_debug('Exception during flashx resolve parse: %s' % e)
            raise
        
    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, 'https://{host}/embed.php?c={media_id}')

    @classmethod
    def get_settings_xml(cls):
        xml = super(cls, cls).get_settings_xml()
        xml.append('<setting id="%s_auto_update" type="bool" label="Automatically update resolver" default="true"/>' % (cls.__name__))
        xml.append('<setting id="%s_etag" type="text" default="" visible="false"/>' % (cls.__name__))
        return xml
