#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
# Caner Candan <caner@candan.fr>, http://caner.candan.fr
#

from .. import API, logging

logger = logging.getLogger("ucoin/ud")


class Ud(API):
    """
    Class relative to the Universal Dividend.
    """
    def __init__(self, conn_handler, module='ud'):
        """
        Constructor

        :param conn_handler: The connection handler.
        :param module: (Default = ud)
        """
        super(Ud, self).__init__(conn_handler, module)


class History(Ud):
    """Get the Universal Dividend history."""

    def __init__(self, conn_handler, pubkey, module='ud'):
        """
        Constructor

        :param conn_handler: The connection handler.
        :param str pubkey: The public key.
        :param module: (Default = ud)
        """
        super(Ud, self).__init__(conn_handler, module)
        self.pubkey = pubkey

    def __get__(self, **kwargs):
        """
        Get the Universal Dividend history.

        :param kwargs:
        """
        assert self.pubkey is not None
        r = yield from self.requests_get('/history/%s' % self.pubkey, **kwargs)
        return (yield from r.json())
