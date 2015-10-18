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

logger = logging.getLogger("ucoin/blockchain")


class Blockchain(API):
    """

    """

    def __init__(self, connection_handler, module='blockchain'):
        """
        Constructor

        :param connection_handler: The connection handler.
        :param str module: (Default value = blockchain)
        """
        super(Blockchain, self).__init__(connection_handler, module)


class Parameters(Blockchain):
    """GET the blockchain parameters used by this node."""

    def __get__(self, **kwargs):
        """
        GET the blockchain parameters used by this node : /blockchain/parameters

        :param kwargs:
        """
        r = yield from self.requests_get('/parameters', **kwargs)
        return (yield from r.json())


class Membership(Blockchain):
    """ GET/POST a Membership document. """

    def __init__(self, connection_handler, search=None):
        """
        Constructor

        :param connection_handler: The connection handler.
        :param search: (Default = None)
        """
        super().__init__(connection_handler)
        self.search = search

    def __post__(self, **kwargs):
        """
        POST a Membership document to the blockchain : /blockchain/membership

        :param kwargs: The field "membership" is required.
        """
        assert 'membership' in kwargs

        r = yield from self.requests_post('/membership', **kwargs)
        return r

    def __get__(self, **kwargs):
        """
        GET a list of Memberships documents issued by the member and written in the blockhain : /blockchain/memberships/[search]

        :param kwargs:
        """
        assert self.search is not None
        r = yield from self.requests_get('/memberships/%s' % self.search, **kwargs)
        return (yield from r.json())


class Block(Blockchain):
    """ GET/POST a block from/to the blockchain. """

    def __init__(self, connection_handler, number=None):
        """
        Constructor - Use the number parameter in order to select a block number.

        :param connection_handler: The connection handler.
        :param int number: The block number to select. (Default = None)
        """
        super(Block, self).__init__(connection_handler)

        self.number = number

    def __get__(self, **kwargs):
        """
        GET a block from the blockchain : /blockchain/block/[NUMBER]

        :param kwargs:
        """
        assert self.number is not None
        r = yield from self.requests_get('/block/%d' % self.number, **kwargs)
        return (yield from r.json())

    def __post__(self, **kwargs):
        """
        POST a block to the blockchain : blockchain/block

        :param kwargs: 2 fields required : field "block" and field "signature".
        """
        assert 'block' in kwargs
        assert 'signature' in kwargs

        r = yield from self.requests_post('/block', **kwargs)
        return r


class Current(Blockchain):
    """ GET, same as block/[number], but return last accepted block. """

    def __get__(self, **kwargs):
        """
        GET, same as block/[number], but return last accepted block : /blockchain/current

        :param kwargs:
        """
        r = yield from self.requests_get('/current', **kwargs)
        return (yield from r.json())


class Hardship(Blockchain):
    """ GET hardship level for given member's fingerprint for writing next block. """

    def __init__(self, connection_handler, fingerprint):
        """
        Constructor - Use the number parameter in order to select a block number.

        :param connection_handler: The connection handler.
        :param str fingerprint: The member fingerprint.
        """
        super(Hardship, self).__init__(connection_handler)

        self.fingerprint = fingerprint

    def __get__(self, **kwargs):
        """
        GET hardship level for given member's fingerprint for writing next block.

        :param kwargs:
        """
        assert self.fingerprint is not None
        r = yield from self.requests_get('/hardship/%s' % self.fingerprint.upper(), **kwargs)
        return (yield from r.json())


class Newcomers(Blockchain):
    """ GET, returns block numbers containing newcomers. """

    def __get__(self, **kwargs):
        """
        GET, returns block numbers containing newcomers : /blockchain/newcomers

        :param kwargs:
        """
        r = yield from self.requests_get('/with/newcomers', **kwargs)
        return (yield from r.json())


class Certifications(Blockchain):
    """ GET, returns block numbers containing certifications. """

    def __get__(self, **kwargs):
        """
        GET, returns block numbers containing certifications.

        :param kwargs:
        """
        r = yield from self.requests_get('/with/certs', **kwargs)
        return (yield from r.json())


class Joiners(Blockchain):
    """ GET, returns block numbers containing joiners. """

    def __get__(self, **kwargs):
        """
        GET, returns block numbers containing joiners.

        :param kwargs:
        """
        r = yield from self.requests_get('/with/joiners', **kwargs)
        return (yield from r.json())


class Actives(Blockchain):
    """ GET, returns block numbers containing actives. """

    def __get__(self, **kwargs):
        """
        GET, returns block numbers containing actives.

        :param kwargs:
        """
        r = yield from self.requests_get('/with/actives', **kwargs)
        return (yield from r.json())


class Leavers(Blockchain):
    """ GET, returns block numbers containing leavers. """

    def __get__(self, **kwargs):
        """
        GET, returns block numbers containing leavers.

        :param kwargs:
        """
        r = yield from self.requests_get('/with/leavers', **kwargs)
        return (yield from r.json())


class Excluded(Blockchain):
    """GET, returns block numbers containing excluded."""

    def __get__(self, **kwargs):
        """
        GET, returns block numbers containing excluded.

        :param kwargs:
        """
        r = yield from self.requests_get('/with/excluded', **kwargs)
        return (yield from r.json())


class UD(Blockchain):
    """GET, returns block numbers containing universal dividend."""

    def __get__(self, **kwargs):
        """
        GET, returns block numbers containing Universal Dividend.

        :param kwargs:
        """
        r = yield from self.requests_get('/with/ud', **kwargs)
        return (yield from r.json())


class TX(Blockchain):
    """GET, returns block numbers containing transactions."""

    def __get__(self, **kwargs):
        """
        GET, returns block numbers containing transactions : /with/tx

        :param kwargs:
        """
        r = yield from self.requests_get('/with/tx', **kwargs)
        return (yield from r.json())
