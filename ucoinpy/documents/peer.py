import re

from ..api.bma import ConnectionHandler
from .document import Document
from .. import PROTOCOL_VERSION, MANAGED_API


class Peer(Document):
    """
    Describing a Peer document.

.. note:: A peer document is specified by the following format :

    | Version: VERSION
    | Type: Peer
    | Currency: CURRENCY_NAME
    | PublicKey: NODE_PUBLICKEY
    | Block: BLOCK
    | Endpoints:
    | END_POINT_1
    | END_POINT_2
    | END_POINT_3
    | [...]
    """

    re_type = re.compile("Type: (Peer)")
    re_pubkey = re.compile("PublicKey: ([1-9A-Za-z][^OIl]{42,45})\n")
    re_block = re.compile("Block: ([0-9]+-[0-9a-fA-F]{5,40})\n")
    re_endpoints = re.compile("Endpoints:\n")

    def __init__(self, version, currency, pubkey, blockid,
                 endpoints, signature):
        """
        Constructor

        :param int version: The uCoin protocol version.
        :param str currency: The currency of the Peer document.
        :param str pubkey: The public key of the node.
        :param str blockid: Block number and hash. Value is used to target a blockchain and precise time reference.
        :param str endpoints: A Mulilines field containing a list of endpoints to interact with the node.
        :param str signature: The signature of the Peer document.
        """
        super().__init__(version, currency, [signature])

        self.pubkey = pubkey
        self.blockid = blockid
        self.endpoints = endpoints

    @classmethod
    def from_signed_raw(cls, raw):
        """

        :param str raw:
        :return:
        :rtype:
        """
        lines = raw.splitlines(True)
        n = 0

        version = int(Peer.re_version.match(lines[n]).group(1))
        n = n + 1

        Peer.re_type.match(lines[n]).group(1)
        n = n + 1

        currency = Peer.re_currency.match(lines[n]).group(1)
        n = n + 1

        pubkey = Peer.re_pubkey.match(lines[n]).group(1)
        n = n + 1

        blockid = Peer.re_block.match(lines[n]).group(1)
        n = n + 1

        Peer.re_endpoints.match(lines[n])
        n = n + 1

        endpoints = []
        while not Peer.re_signature.match(lines[n]):
            endpoint = Endpoint.from_inline(lines[n])
            endpoints.append(endpoint)
            n = n + 1

        signature = Peer.re_signature.match(lines[n]).group(1)

        return cls(version, currency, pubkey, blockid, endpoints, signature)

    def raw(self):
        """
        Get the Peer document in a raw format,

        :return: The Peer document as a string document.
        :rtype: str
        """
        doc = """Version: {0}
                Type: Peer
                Currency: {1}
                PublicKey: {2}
                Block: {3}
                Endpoints:
                """.format(self.version, self.currency, self.pubkey, self.blockid)

        for endpoint in self.endpoints:
            doc += "{0}\n".format(endpoint.inline())

        doc += "{0}\n".format(self.signatures[0])
        return doc


class Endpoint():
    """
    Describing EndPoints

.. note:: This document can be specified by this following format :

    | NAME_OF_THE_API [DNS] [IPv4] [IPv6] [PORT]
    """

    @staticmethod
    def from_inline(inline):
        """
        Creates a Endpoint from an inline format.

        :param str inline: The inline Endpoint.
        :return: The inline Endpoint.
        :rtype: Endpoint
        """
        for api in MANAGED_API:
            if (inline.startswith(api)):
                if (api == "BASIC_MERKLED_API"):
                    return BMAEndpoint.from_inline(inline)
        return UnknownEndpoint.from_inline(inline)


class UnknownEndpoint(Endpoint):
    """
    Describing an UnknownEndpoint
    """

    def __init__(self, api, properties):
        """
        Constructor

        :param api: The API
        :param properties:
        """
        self.api = api
        self.properties = properties

    @classmethod
    def from_inline(cls, inline):
        """
        Creates an UnknownEndpoint from an inline format.

        :param str inline: The inline UnknownEndpoint.
        :return: The inline UnknownEndpoint.
        :rtype: UnknownEndpoint
        """
        api = inline.split()[0]
        properties = inline.split()[1:]
        return cls(api, properties)

    def inline(self):
        """
        Get the UnknownEndpoint in an inline format,

        :return: The UnknownEndpoint as an inline string.
        :rtype: str
        """
        doc = self.api
        for p in self.properties:
            doc += " {0}".format(p)
        return doc


class BMAEndpoint(Endpoint):
    """
    Describing a BMAEndpoint

.. note:: This document is specified by the following format :

    | BASIC_MERKLED_API [DNS] [IPv4] [IPv6] [PORT]
    """

    re_inline = re.compile('^BASIC_MERKLED_API(?: ([a-z0-9-_.]*(?:.[a-zA-Z])))?(?: ((?:[0-9.]{1,4}){4}))?(?: ((?:[0-9a-f:]{4,5}){4,8}))?(?: ([0-9]+))$')

    @classmethod
    def from_inline(cls, inline):
        """
        Get a BMAEndpoint from an inline format.

        :param str inline: The inline BMAEndpoint.
        :return: The inline BMAEndpoint.
        :rtype: BMAEndpoint
        """
        m = BMAEndpoint.re_inline.match(inline)
        server = m.group(1)
        ipv4 = m.group(2)
        ipv6 = m.group(3)
        port = int(m.group(4))
        return cls(server, ipv4, ipv6, port)

    def __init__(self, server, ipv4, ipv6, port):
        """
        Constructor

        :param str server: The URL of the node.
        :param str ipv4: The IPV4 address of the node.
        :param str ipv6: The IPV4 address of the node.
        :param int port: The port of the node.
        """
        self.server = server
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.port = port

    def inline(self):
        """
        Get the BMAEndpoint in an inline format,

        :return: The BMAEndpoint as an inline string.
        :rtype: str
        """
        return "BASIC_MERKLED_API{DNS}{IPv4}{IPv6}{PORT}" \
                    .format(DNS=(" {0}".format(self.server) if self.server else ""),
                            IPv4=(" {0}".format(self.ipv4) if self.ipv4 else ""),
                            IPv6=(" {0}".format(self.ipv6) if self.ipv6 else ""),
                            PORT=(" {0}".format(self.port) if self.port else ""))

    def conn_handler(self):
        """
        Handles the connection's informations.
        """
        if self.server:
            return ConnectionHandler(self.server, self.port)
        elif self.ipv4:
            return ConnectionHandler(self.ipv4, self.port)
        else:
            return ConnectionHandler(self.ipv6, self.port)
