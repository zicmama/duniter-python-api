import re
import base64
import logging

from .document import Document


class SelfCertification(Document):
    """
    A document describing a self-Certification.

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

        :param int version: uCoin protocol version.
        :param str currency: The self-Certification currency target.
        :param str pubkey: The pubkey which is self-certified.
        :param int ts: The timestamp of the self-Certification.
        :param str uid: The uid which is self-certified.
        :param str signature: The signature of the self-Certification.
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
        Creates a SelfCertification from an inline format.

.. note :: An inline self-certification is specified by the following format :

        | PUBLIC_KEY:SIGNATURE:TIMESTAMP:USER_ID

        :param int version: uCoin protocol version.
        :param str currency: The self-Certification currency target.
        :param str inline: The inline self-Certification.
        :return: The inline self-Certification.
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

        :return: The self-Certification as a string document.
        :rtype: str
        """
        return """UID:{0}
META:TS:{1}
""".format(self.uid, self.timestamp)

    def inline(self):
        """
        Get the SelfCertification in an inline format,

        :return: The self-Certification as an inline string.
        :rtype: str
        """
        return "{0}:{1}:{2}:{3}".format(self.pubkey, self.signatures[0],
                                    self.timestamp, self.uid)


class Certification(Document):
    """
    A document describing a Certification.

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

        :param int version: uCoin protocol version.
        :param str currency: the self certification currency target.
        :param str pubkey_from: the pubkey which is certifying.
        :param str pubkey_to: the pubkey which is certified.
        :param int blocknumber: The block number of the Certification.
        :param str blockhash: the block hash of the certification.
        :param str signature: the signature of the certification.
        """
        super().__init__(version, currency, [signature])
        self.pubkey_from = pubkey_from
        self.pubkey_to = pubkey_to
        self.blockhash = blockhash
        self.blocknumber = blocknumber

    @classmethod
    def from_inline(cls, version, currency, blockhash, inline):
        """
        Get a Certification from an inline format.

.. note :: An inline Certification is specified by the following format :

        | PUBKEY_FROM:PUBKEY_TO:BLOCK_NUMBER:SIGNATURE

        :param int version: uCoin protocol version.
        :param str currency: The Certification currency target.
        :param  blockhash: The block number of the Certification.
        :param str inline: The inline Certification.
        :return: The inline Certification.
        :rtype: Certification
        """
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
        """
        Get the Certification in a raw format,
        :return: The Certification as a string document.
        :rtype: str
        """
        return """{0}META:TS:{1}-{2}
""".format(selfcert.signed_raw(), self.blocknumber, self.blockhash)

    def sign(self, selfcert, keys):
        """
        Sign the current document.
        Warning : Current signatures will be replaced with the new ones.
        """
        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(selfcert), 'ascii')))
            logging.debug("Signature : \n{0}".format(signing.decode("ascii")))
            self.signatures.append(signing.decode("ascii"))

    def signed_raw(self, selfcert):
        """
        If keys are None, returns the raw + current signatures.
        If keys are present, returns the raw signed by these keys.

        :param str raw:
        :return:
        :rtype:
        """
        raw = self.raw(selfcert)
        signed = "\n".join(self.signatures)
        signed_raw = raw + signed + "\n"
        return signed_raw

    def inline(self):
        """
        Get the Certification in an inline format,
        :return: The Certification as an inline string.
        :rtype: str
        """
        return "{0}:{1}:{2}:{3}".format(self.pubkey_from, self.pubkey_to,
                                        self.blocknumber, self.signatures[0])


class Revocation(Document):
    """
    A document describing a self-Revocation.

.. note:: This document is specified by the following format :

    | UID:IDENTIFIER
    | META:TS:TIMESTAMP
    | SIGNATURE
    | META:REVOKE
    | CERTIFIER_SIGNATURE
    """
    def __init__(self, version, currency, signature):
        """
        Constructor

        :param int version: uCoin protocol version.
        :param str currency: The self-Revocation currency target.
        :param str signature: the signature of the self-Revocation.
        """
        super().__init__(version, currency, [signature])

    def raw(self, selfcert):
        """
        Get the Self-Revocation in a raw format,
        :return: The self-Revocation as a string document.
        :rtype: str
        """
        return """{0}META:REVOKE""".format(selfcert.signed_raw())

    def sign(self, selfcert, keys):
        """
        Sign the current document.
        Warning : Current signatures will be replaced with the new ones.
        """
        self.signatures = []
        for key in keys:
            signing = base64.b64encode(key.signature(bytes(self.raw(selfcert), 'ascii')))
            self.signatures.append(signing.decode("ascii"))
