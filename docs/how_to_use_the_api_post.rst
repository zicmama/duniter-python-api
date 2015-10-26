How to use uCoinPy to POST specified data
--------------------------------------------------------

* ``/wot/add``
* ``/wot/revoke``

\

* ``/blockchain/membership``
* ``/blockchain/block``

\

* ``/network/peering/peers``

\

* ``/tx/process``



Imports and initializations of variables :

.. code-block:: python

  import aiohttp, asyncio, ucoinpy

  # You can use either complete defined endpoint with IPV4 or with IPV6 ; or the simple definition : domain name + port number.

  # Given node : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] PORT]
  # or
  # Given node : [NAME_OF_THE_API] [DOMAIN] [PORT]
  myEndpoint = "BASIC_MERKLED_API metab.ucoin.io 9201"

  myPubKeyMB = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/wot/add``

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#wotadd


.. code-block:: python

  # ---------- POST Public key data. ------------


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/wot/revoke``

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#wotrevoke


.. code-block:: python

  # ----------- Remove an identity from Identity pool.  N.B.: An identity written in the blockchain cannot be removed. ---------


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/blockchain/membership``

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#blockchainmembership


.. code-block:: python

  # ----------- POST a Membership document. -------------


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/blockchain/block``

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#blockchainblock


.. code-block:: python

  # ----------- POST a new block to add to the blockchain. -------------


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/network/peering/peers``

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#networkpeeringpeers-post


.. code-block:: python

  # ----------- POST a UCG peering entry document to this node in order to alter UCG peering table. -------------


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/tx/process``

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#txprocess


.. code-block:: python

  # ----------- POST a transaction. -----------
