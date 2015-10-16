import re
import base64
import logging

from .document import Document


class SelfCertification(Document):
    """
    A document describing a self certification.

.. note:: This document is specified by the following format :

    | UID:IDENTIFIER
    | META:TS:TIMESTAMP
    | SIGNATURE

    """

    re_inline = re.compile("([1-9A-Za-z][^OIl]{42,45}):([A-Za-z0-9+/]+(?:=|==)?):([0-9]+):([^\n]+)\n")
    re_uid = re.compile("UID:([^\n]+)\n")
    re_timestamp = re.compile("META:TS:([0-9]+)\n")

    def __init__(self, version, currency, pubkey, ts, uid, signature):
        """
        Constructor of a SelfCertification

        :param int version: ucoin protocol version
        :param str currency: the self certification currency target
        :param str pubkey: the pubkey which is self-certified
        :param int ts: the timestamp of the self-certification
        :param str uid: the uid which is self-certified
        :param str signature: the signature of the self-certification
        """
        if signature:
            super().__init__(version, currency, [signature])
        else:
            super().__init__(version, currency, [])
        self.pubkey = pubkey
        self.timestamp = ts
        self.uid = uid

    @classmethod
    def from_inline(cls, version, currency, inline):
        """
        Creates a SelfCertification from an inline format

.. note :: An inline self certification is specified by the following format :
PUBLIC_KEY:SIGNATURE:TIMESTAMP:USER_ID

        :param int version: ucoin protocol version
        :param str currency: the self certification currency target
        :param str inline: the inline self-certification
        :return: the inline SelfCertification
        :rtype: SelfCertification
        """
        selfcert_data = SelfCertification.re_inline.match(inline)
        pubkey = selfcert_data.group(1)
        signature = selfcert_data.group(2)
        ts = int(selfcert_data.group(3))
        uid = selfcert_data.group(4)
        return cls(version, currency, pubkey, ts, uid, signature)

    def raw(self):
        """
        Get the SelfCertification in a raw format,
        :return: the self certification as a string document
        :rtype: str
        """
        return """UID:{0}
META:TS:{1}
""".format(self.uid, self.timestamp)

    def inline(self):
        """
        Get the SelfCertification in an inline format,
        :return: the self certification as an inline string
        :rtype: str
        """
        return "{0}:{1}:{2}:{3}".format(self.pubkey, self.signatures[0],
                                    self.timestamp, self.uid)


class Certification(Document):
    """
    A document describing a certification.

..note:: This document is defined by the following format :

     | UID:IDENTIFIER
     | META:TS:TIMESTAMP
     | SIGNATURE
     | META:TS:BLOCK_NUMBER-BLOCK_HASH
     | CERTIFIER_SIGNATURE

    """

    re_inline = re.compile("([1-9A-Za-z][^OIl]{42,45}):([1-9A-Za-z][^OIl]{42,45}):([0-9]+):([A-Za-z0-9+/]+(?:=|==)?)\n")
    re_timestamp = re.compile("META:TS:([0-9]+)-([0-9a-fA-F]{5,40})\n")

    def __init__(self, version, currency, pubkey_from, pubkey_to,
                 blocknumber, blockhash, signature):
        """
        Constructor

        :param int version: ucoin protocol version
        :param str currency: the self certification currency target
        :param str pubkey_from: the pubkey which is certifying
        :param str pubkey_to: the pubkey which is certified
        :param int blocknumber: the block number of the certification
        :param str blockhash: the block hash of the certification
        :param str signature: the signature of the certification
        """
        super().__init__(version, currency, [signature])
        self.pubkey_from = pubkey_from
        self.pubkey_to = pubkey_to
        self.blockhash = blockhash
        self.blocknumber = blocknumber

    @classmethod
    def from_inline(cls, version, currency, blockhash, inline):
        cert_data = Certification.re_inline.match(inline)
        pubkey_from = cert_data.group(1)
        pubkey_to = cert_data.group(2)
        blocknumber = int(cert_data.group(3))
        if blocknumber == 0:
            blockhash = "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709"
        signature = cert_data.group(4)
        return cls(version, currency, pubkey_from, pubkey_to,
                   blocknumber, blockhash, signature)

    def raw(self, selfcert):
        return """{0}META:TS:{1}-{2}
""".format(selfcert.signed_raw(), self.blocknumber, self.blockhash)

    def sign(self, selfcert, keys):
        """
        Sign the current document.
        Warning : current signatures will be replaced with the new ones.
        """
        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(selfcert), 'ascii')))
            logging.debug("Signature : \n{0}".format(signing.decode("ascii")))
            self.signatures.append(signing.decode("ascii"))

    def signed_raw(self, selfcert):
        raw = self.raw(selfcert)
        signed = "\n".join(self.signatures)
        signed_raw = raw + signed + "\n"
        return signed_raw

    def inline(self):
        return "{0}:{1}:{2}:{3}".format(self.pubkey_from, self.pubkey_to,
                                        self.blocknumber, self.signatures[0])


class Revocation(Document):
    """
    A document describing a self-revocation.
    """
    def __init__(self, version, currency, signature):
        """
        Constructor
        """
        super().__init__(version, currency, [signature])

    def raw(self, selfcert):
        return """{0}META:REVOKE
""".format(selfcert.signed_raw())

    def sign(self, selfcert, keys):
        """
        Sign the current document.
        Warning : current signatures will be replaced with the new ones.
        """
        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(selfcert), 'ascii')))
            self.signatures.append(signing.decode("ascii"))

