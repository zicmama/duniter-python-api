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
# Inso <insomniak.fr at gmail.com>


__all__ = ['api']

PROTOCOL_VERSION = "1"

import aiohttp, asyncio, logging, json

logger = logging.getLogger("ucoin")


class ConnectionHandler(object):
    """Helper class used by other API classes to ease passing node connection information."""

    def __init__(self, server, port):
        """
        Constructor

        :param str server: The node hostname.
        :param int port: The port number.
        """

        self.server = server
        self.port = port

    def __str__(self):
        """
        Get connection information.
        """
        return 'Connection info: %s:%d' % (self.server, self.port)


class API(object):
    """APIRequest is a class used as an interface. The intermediate derivated classes are the modules and the leaf classes are the API requests."""

    def __init__(self, connection_handler, module):
        """
        Constructor - Asks a module in order to create the URL used then by derivated classes.

        :param connection_handler: The connection handler.
        :param str module: The module name.
        """

        self.module = module
        self.connection_handler = connection_handler
        self.headers = {}

    def reverse_url(self, path):
        """
        Reverses the URL using self.url and a given path in parameter.

        :param path: The request path.
        """

        server, port = self.connection_handler.server, self.connection_handler.port

        url = 'http://%s:%d/%s' % (server, port, self.module)
        return url + path

    def get(self, **kwargs):
        """A wrapper of overloaded __get__ method."""

        return self.__get__(**kwargs)

    def post(self, **kwargs):
        """A wrapper of overloaded __post__ method."""

        logger.debug('do some work with')

        data = self.__post__(**kwargs)

        logger.debug('and send back')

        return data

    def __get__(self, **kwargs):
        """An interface purpose for GET request."""
        pass

    def __post__(self, **kwargs):
        """An interface purpose for POST request."""
        pass

    @asyncio.coroutine
    def requests_get(self, path, **kwargs):
        """
        Requests GET wrapper in order to use API parameters.

        :param path: The request path.
        """
        logging.debug("Request : {0}".format(self.reverse_url(path)))
        response = yield from asyncio.wait_for(aiohttp.get(self.reverse_url(path), params=kwargs,
                                headers=self.headers), 15)

        if response.status != 200:
            raise ValueError('status code != 200 => %d (%s)' % (response.status, (yield from response.text())))

        return response

    def requests_post(self, path, **kwargs):
        """
        Requests POST wrapper in order to use API parameters.

        :param path: The request path.
        """
        if 'self_' in kwargs:
            kwargs['self'] = kwargs.pop('self_')

        logging.debug("POST : {0}".format(kwargs))
        response = yield from asyncio.wait_for(
            aiohttp.post(self.reverse_url(path), data=kwargs, headers=self.headers),
                                 timeout=15)

        if response.status != 200:
            raise ValueError('status code != 200 => %d (%s)' % (response.status, (yield from (response.text()))))

        return response

from . import network, blockchain, tx, wot, node, ud
