"""
Created on 2 déc. 2014

@author: inso
"""
from .. import PROTOCOL_VERSION
from .document import Document

import re


class Membership(Document):
    """
    A document describing a Membership.

.. note:: A membership document is specified by the following format :

    | Version: VERSION
    | Type: Membership
    | Currency: CURRENCY_NAME
    | Issuer: ISSUER
    | Block: NUMBER-HASH
    | Membership: MEMBERSHIP_TYPE
    | UserID: USER_ID
    | CertTS: CERTIFICATION_TS

    """

    # PUBLIC_KEY:SIGNATURE:NUMBER:HASH:TIMESTAMP:USER_ID
    re_inline = re.compile("([1-9A-Za-z][^OIl]{42,45}):([A-Za-z0-9+/]+(?:=|==)?):\
([0-9]+):([0-9a-fA-F]{5,40}):([0-9]+):([^\n]+)\n")
    re_type = re.compile("Type: (Membership)")
    re_issuer = re.compile("Issuer: ([1-9A-Za-z][^OIl]{42,45})\n")
    re_block = re.compile("Block: ([0-9]+)-([0-9a-fA-F]{5,40})\n")
    re_membership_type = re.compile("Membership: (IN|OUT)")
    re_userid = re.compile("UserID: ([^\n]+)\n")
    re_certts = re.compile("CertTS: ([0-9]+)\n")



    def __init__(self, version, currency, issuer, block_number, block_hash,
                 membership_type, uid, cert_ts, signature):
        """
        Constructor

        :param int version: The uCoin protocol version.
        :param str currency: The Membership currency target.
        :param  issuer: The public key of the issuer.
        :param  block_number:
        :param  block_hash:
        :param  membership_type: Membership message. Value is either IN or OUT to express wether a member wishes to opt-in or opt-out the community.
        :param  uid: Identity to use for this public key.
        :param  cert_ts: Identity's certification date.
        :param str signature: The signature of the Membership document.
        """
        super().__init__(version, currency, [signature])
        self.issuer = issuer
        self.block_number = block_number
        self.block_hash = block_hash
        self.membership_type = membership_type
        self.uid = uid
        self.cert_ts = cert_ts

    @classmethod
    def from_inline(cls, version, currency, membership_type, inline):
        """
        Creates a Membership from an inline format.

        :param int version: uCoin protocol version.
        :param str currency: The Membership currency target.
        :param membership_type:  Membership message. Value is either IN or OUT to express wether a member wishes to opt-in or opt-out the community.
        :param str inline: The inline Membership.
        :return: The inline Membership.
        :rtype: Membership
        """
        data = Membership.re_inline.match(inline)
        issuer = data.group(1)
        signature = data.group(2)
        block_number = int(data.group(3))
        block_hash = data.group(4)
        cert_ts = int(data.group(5))
        uid = data.group(6)
        return cls(version, currency, issuer, block_number,
                   block_hash, membership_type, uid, cert_ts, signature)

    @classmethod
    def from_signed_raw(cls, raw, signature=None):
        """

        :param str raw:
        :return:
        :rtype:
        """
        lines = raw.splitlines(True)
        n = 0

        version = int(Membership.re_version.match(lines[n]).group(1))
        n = n + 1

        Membership.re_type.match(lines[n]).group(1)
        n = n + 1

        currency = Membership.re_currency.match(lines[n]).group(1)
        n = n + 1

        issuer = Membership.re_issuer.match(lines[n]).group(1)
        n = n + 1

        blockid = Membership.re_block.match(lines[n])
        blocknumber = int(blockid.group(1))
        blockhash = blockid.group(2)
        n = n + 1

        membership_type = Membership.re_membership_type.match(lines[n]).group(1)
        n = n + 1

        uid = Membership.re_userid.match(lines[n]).group(1)
        n = n + 1

        cert_ts = int(Membership.re_certts.match(lines[n]).group(1))
        n = n + 1

        signature = Membership.re_signature.match(lines[n]).group(1)
        n = n + 1

        return cls(version, currency, issuer, blocknumber, blockhash,
                   membership_type, uid, cert_ts, signature)

    def raw(self):
        """
        Get the Membership in a raw format,
        :return: The Membership as a string document.
        :rtype: str
        """
        return """Version: {0}
                    Type: Membership
                    Currency: {1}
                    Issuer: {2}
                    Block: {3}-{4}
                    Membership: {5}
                    UserID: {6}
                    CertTS: {7}
                    """.format(self.version,
                      self.currency,
                      self.issuer,
                      self.block_number, self.block_hash,
                      self.membership_type,
                      self.uid,
                      self.cert_ts)

    def inline(self):
        """
        Get the Membership in an inline format,
        :return: The Membership as an inline string.
        :rtype: str
        """
        return "{0}:{1}:{2}:{3}:{4}:{5}".format(self.issuer,
                                        self.signatures[0],
                                        self.block_number,
                                        self.block_hash,
                                        self.cert_ts,
                                        self.uid)
