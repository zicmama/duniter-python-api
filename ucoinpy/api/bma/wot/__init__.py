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

logger = logging.getLogger("ucoin/wot")


class WOT(API):
    def __init__(self, connection_handler, module='wot'):
        super(WOT, self).__init__(connection_handler, module)


class Add(WOT):
    """POST Public key data."""

    def __post__(self, **kwargs):
        assert 'pubkey' in kwargs
        assert 'self_' in kwargs
        assert 'other' in kwargs

        r = yield from self.requests_post('/add', **kwargs)
        return r


class Revoke(WOT):
    """POST Public key data."""

    def __post__(self, **kwargs):
        assert 'pubkey' in kwargs
        assert 'self_' in kwargs

        r = yield from self.requests_post('/revoke', **kwargs)
        return r


class Lookup(WOT):
    """GET Public key data."""
    schema = {
        "type": "object",
        "definitions": {
            "meta_data": {
                "type": "object",
                "properties": {
                    "timestamp": {
                        "type": "number"
                    }
                }
            },
        },
        "properties": {
            "partial": {
                "type": "boolean"
            },
            "results": {
                "type": "array",
                "item": {
                    "type": "object",
                    "properties": {
                        "pubkey": {
                            "type": "string"
                        }
                    },
                    "uids": {
                        "type": "array",
                        "item": {
                            "type": "object",
                            "properties": {
                                "uid": {
                                    "type": "string"
                                },
                                "meta": {
                                    "$ref": "#/definitions/meta_data"
                                },
                                "self": {
                                    "type": "string",
                                },
                                "others": {
                                    "type": "array",
                                    "item": {
                                        "type": "object",
                                        "properties": {
                                            "pubkey": {
                                                "type": "string",
                                            },
                                            "meta": {
                                                "$ref": "#/definitions/meta_data"
                                            },
                                            "signature": {
                                                "type": "string"
                                            }
                                        }
                                    }
                                }
                            },
                            "required": ["uid", "meta", "self", "others"]
                        }
                    },
                    "signed": {
                        "type": "array",
                        "item": {
                            "type": "object",
                            "properties": {
                                "uid": {
                                    "type": "string"
                                },
                                "pubkey": {
                                    "type": "string"
                                },
                                "meta": {
                                    "$ref": "#/definitions/meta_data"
                                },
                                "signature": {
                                    "type": "string"
                                }
                            },
                            "required": ["uid", "pubkey", "meta", "signature"]
                        }
                    },
                    "required": ["uids", "signed"]
                }
            }
        },
        "required": ["partial", "results"]
    }

    def __init__(self, connection_handler, search, module='wot'):
        super(WOT, self).__init__(connection_handler, module)

        self.search = search

    def __get__(self, **kwargs):
        assert self.search is not None

        r = yield from self.requests_get('/lookup/%s' % self.search, **kwargs)
        return (yield from r.json())


class CertifiersOf(WOT):
    """GET Certification data over a member."""

    schema = {
        "type": "object",
        "properties": {
            "pubkey": {
                "type": "string"
            },
            "uid": {
                "type": "string"
            },
            "isMember": {
                "type": "boolean"
            },
            "certifications": {
                "type": "array",
                "item": {
                    "type": "object",
                    "properties": {
                        "pubkey": {
                            "type": "string"
                        },
                        "uid": {
                            "type": "string"
                        },
                        "cert_time": {
                            "type": "object",
                            "properties": {
                                "block": {
                                    "type": "number"
                                },
                                "medianTime": {
                                    "type": "number"
                                }
                            },
                            "required": ["block", "medianTime"]
                        },
                        "written": {
                            "type": "object",
                            "properties": {
                                "number": {
                                    "type": "number",
                                },
                                "hash": {
                                    "type": "string"
                                }
                            },
                            "required": ["number", "hash"]
                        },
                        "isMember": {
                            "type": "boolean"
                        },
                        "signature": {
                            "type": "string"
                        }
                    },
                    "required": ["pubkey", "uid", "cert_time", "written", "isMember", "signature"]
                }
            }
        },
        "required": ["pubkey", "uid", "isMember", "certifications"]
    }

    def __init__(self, connection_handler, search, module='wot'):
        super(WOT, self).__init__(connection_handler, module)

        self.search = search

    def __get__(self, **kwargs):
        assert self.search is not None

        r = yield from self.requests_get('/certifiers-of/%s' % self.search, **kwargs)
        return (yield from r.json())


class CertifiedBy(WOT):
    """GET Certification data from a member."""

    schema = CertifiersOf.schema

    def __init__(self, connection_handler, search, module='wot'):
        super(WOT, self).__init__(connection_handler, module)

        self.search = search

    def __get__(self, **kwargs):
        assert self.search is not None

        r = yield from self.requests_get('/certified-by/%s' % self.search, **kwargs)
        return (yield from r.json())


class Members(WOT):
    """GET List all current members of the Web of Trust."""
    schema = {
        "type": "object",
        "properties": {
            "results": {
                "type": "array",
                "item": {
                    "type": "object",
                    "properties": {
                        "pubkey": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }

    def __init__(self, connection_handler, module='wot'):
        super(WOT, self).__init__(connection_handler, module)

    def __get__(self, **kwargs):
        r = yield from self.requests_get('/members', **kwargs)
        return (yield from r.json())
