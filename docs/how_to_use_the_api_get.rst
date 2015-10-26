How to use the Python uCoin API to Get specified data
--------------------------------------------------------

* ``/node/summary``

* ``/blockchain/parameters``

* ``/blockchain/current``

\

* ``/network/peering``

* ``/network/peering/peers``

\

* ``/wot/loookup/[pubkey]``

* ``/wot/requirements/[pubkey]``

* ``/wot/certifiers-of/[pubkey]``

* ``/wot/certified-by/[pubkey]``

* ``/blockchain/memberships/[pubkey]``

* ``/blockchain/hardship/[pubkey]``

* ``/tx/sources/[pubkey]``

* ``/tx/history/[pubkey]``

* ``/ud/history/[pubkey]``

\

* ``/blockchain/block/[NUMBER]``

* ``/tx/history/[PUBKEY]/blocks/[FROM]/[TO]``

* ``/tx/history/[PUBKEY]/times/[FROM]/[TO]``



**Imports and initializations of variables :**

.. code-block:: python

  import aiohttp, asyncio, ucoinpy

  # You can use either a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
  # or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
  myEndpoint = "BASIC_MERKLED_API metab.ucoin.io 9201"


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/node/summary`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#nodesummary


.. code-block:: python

  # ----- GET technical informations about this peer. -----------
  nodeSummary = ""

  # Get the informations /node/summary from the given node :
  def getNodeSummary():
      global nodeSummary
      # Here we request for the path /node/ "summary" through the "Basic Merkled API"
      nodeSummary = yield from Summary(Endpoint.from_inline(myEndpoint).conn_handler()).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getNodeSummary())

  print("\nnodeSummary : ")
  print(nodeSummary)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/blockchain/parameters`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#blockchainparameters

.. code-block:: python

  # ----- GET the blockchain parameters used by this node. -----------
  blockchainParameters = ""

  # Get the informations /blockchain/parameters from the given node :
  # Information of the blockchain or currency
  def getBlockchainParameters():
      global blockchainParameters
      # Here we request for the path /blockchain/ "parameters" through the "Basic Merkled API"
      blockchainParameters = yield from Parameters(Endpoint.from_inline(myEndpoint).conn_handler()).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getBlockchainParameters())

  # ----- Display general info on the currency network -----------
  # Call the asynchronous function :
  print("\nblockchainParameters :")
  print(blockchainParameters)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/blockchain/current`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#blockchaincurrent

.. code-block:: python

  # ----- Same as block/[number], but return last accepted block. -----------

  # Can generate an error on an empty blockchain, if the network has not yet certified peers.
  blockchainCurrent = ""

  # Get the informations /blockchain/current from the given node :
  # Information of the last computed block.
  def getBlockchainCurrent():
      global blockchainCurrent
      # Here we request for the path /blockchain/ "current" through the "Basic Merkled API"
      blockchainCurrent = yield from Current(Endpoint.from_inline(myEndpoint).conn_handler()).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getBlockchainCurrent())

  print("\nblockchainCurrent :")
  print(blockchainCurrent)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/network/peering`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#networkpeering

.. code-block:: python

  # ----- GET the peering informations of this node. -----------
  networkPeering = ""

  # Get the informations /network/peering from the given node :
  def getNetworkPeering():
      global networkPeering
      # Here we request for the path /network/ "peering" through the "Basic Merkled API"
      networkPeering = yield from Peering(Endpoint.from_inline(myEndpoint).conn_handler()).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getNetworkPeering())

  print("\nnetworkPeering :")
  print(networkPeering)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/network/peering/peers`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#networkpeeringpeers-get

.. code-block:: python

  # ----- Merkle URL refering to peering entries of every node inside the currency network. -----------
  peeringPeers = ""

  # Get the informations /network/peering/peers from the given node :
  def getNetworkPeeringPeers():
    global peeringPeers
    # Here we request for the path /network/peering/ "peers" through the "Basic Merkled API"
    peeringPeers = yield from Peers(Endpoint.from_inline(myEndpoint).conn_handler()).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getNetworkPeeringPeers())

  print("\npeeringPeers :")
  print(peeringPeers)



\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


Get information from the blockchain with a given public key :


``/wot/loookup/[pubkey]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#wotlookupsearch

.. code-block:: python

  # -------------- GET Public key data. -------------

  myPubKeyMB = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
  wotLookup = ""

  # Get the informations /wot/lookup/[pubkey] from the given node :
  # Information on the given public key.
  def getWotLookup():
      global wotLookup
      # Here we request for the path /wot/ "lookup/[pubkey]" through the "Basic Merkled API"
      wotLookup = yield from Lookup(Endpoint.from_inline(myEndpoint).conn_handler(), myPubKey).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getWotLookup())

  print("\nwotLookup :")
  print(wotLookup)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/wot/requirements/[pubkey]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#networkpeeringpeers-get

.. code-block:: python

  # ------- GET requirements to be filled by pubkey to become a member. ----

  # Not yet implemented in the Python API : /wot/requirements

  myPubKeyMB = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
  wotRequirements = ""

  # Get the informations /wot/requirements/[pubkey] from the given node :
  # Information on the given public key.

  def getWotRequirements():
      global wotRequirements
      # Here we request for the path /wot/ "requirements/[pubkey]" through the "Basic Merkled API"
      wotRequirements = yield from Requirements(Endpoint.from_inline(myEndpoint).conn_handler(), myPubKey).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getWotRequirements())

  print("\nwotRequirements :")
  print(wotRequirements)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/wot/certifiers-of/[pubkey]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#wotcertifiers-ofsearch

.. code-block:: python

  # -------------- GET Certification data over a member. -------------

  # Can generate an error on an empty blockchain, if the network has not yet certified peers.

  myPubKeyMB = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
  wotCertifiersOf = ""

  # Get the informations /wot/certifiers-of/[pubkey] from the given node :
  # Information on the given public key : the certifiers
  def getWotCertifiersOf():
      global wotCertifiersOf
      # Here we request for the path /wot/ "certifiers-of/[pubkey]" through the "Basic Merkled API"
      wotCertifiersOf = yield from CertifiersOf(Endpoint.from_inline(myEndpoint).conn_handler(), myPubKey).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getWotCertifiersOf())

  print("\nwotCertifiersOf :")
  print(wotCertifiersOf)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/wot/certified-by/[pubkey]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#wotcertified-bysearch

.. code-block:: python

  # -------------- GET Certification data over a member. -------------

  # Can generate an error on an empty blockchain, if the network has not yet certified peers.

  myPubKeyMB = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
  wotCertifiedBy = ""

  # Get the informations /wot/certified-by/[pubkey] from the given node :
  # Information on the given public key : the certified by this public key.
  def getWotCertifiedBy():
    global wotCertifiedBy
    # Here we request for the path /wot/ "certified-by/[pubkey]" through the "Basic Merkled API"
    wotCertifiedBy = yield from CertifiedBy(Endpoint.from_inline(myEndpoint).conn_handler(), myPubKey).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getWotCertifiedBy())

  print("\nwotCertifiedBy :")
  print(wotCertifiedBy)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/blockchain/memberships/[pubkey]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#blockchainmembershipssearch

.. code-block:: python

  # -------- GET Membership data written for a member. ----------------

  # Can generate an error on an empty blockchain, if the network has not yet certified peers.

  myPubKeyMB = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
  blockchainMemberships = ""

  # Get the informations /blockchain/memberships/[pubkey] from the given node :
  # Information on the given public key : the memberships of this public key.
  def getBlockchainMemberships():
      global blockchainMemberships
      # Here we request for the path /blockchain/ "memberships/[pubkey]" through the "Basic Merkled API"
      blockchainMemberships = yield from Membership(Endpoint.from_inline(myEndpoint).conn_handler(), myPubKey).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getBlockchainMemberships())

  print("\nblockchainMemberships :")
  print(blockchainMemberships)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/blockchain/hardship/[pubkey]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#blockchainhardshippubkey

.. code-block:: python

  # --------------- GET hardship level for given member's pubkey for writing next block. -----------

  myPubKeyMB = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
  blockchainHardship = ""

  # Get the informations /blockchain/hardship/[pubkey] from the given node :
  # Information on the given public key : the hardship ? of this public key.
  def getBlockchainHardship():
    global blockchainHardship
    # Here we request for the path /blockchain/ "hardship/[pubkey]" through the "Basic Merkled API"
    blockchainHardship = yield from Hardship(Endpoint.from_inline(myEndpoint).conn_handler(), myPubKey).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getBlockchainHardship())

  print("\nblockchainHardship :")
  print(blockchainHardship)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/tx/sources/[pubkey]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#txsourcespubkey

.. code-block:: python

  # ----------- GET a list of available sources. -----------

  myPubKeyMB = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
  txSources = ""

  # Get the informations /tx/sources/[pubkey] from the given node :
  # Information on the tx : inputs and outputs.
  def getTxSources():
      global txSources
      # Here we request for the path /tx/ "sources/[pubkey]" through the "Basic Merkled API"
      txSources = yield from Sources(Endpoint.from_inline(myEndpoint).conn_handler(), myPubKey).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getTxSources())

  print("\ntxSources :")
  print(txSources)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/tx/history/[pubkey]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#txhistorypubkey

.. code-block:: python

  # ----------- Get the wallet transaction history. -----------

  myPubKeyMB = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
  txHistory = ""

  # Get the informations /tx/history/[pubkey] from the given node :
  # The history of the transactions ( tx )
  def getTxHistory():
      global txHistory
      # Here we request for the path /tx/ "history/[pubkey]" through the "Basic Merkled API"
      txHistory = yield from tx.History(Endpoint.from_inline(myEndpoint).conn_handler(), myPubKey).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getTxHistory())

  print("\ntxHistory :")
  print(txHistory)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/ud/history/[pubkey]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#udhistorypubkey

.. code-block:: python

  # ----------- Get the wallet universal dividend history. -----------

  # Can generate an error on an empty blockchain, if the network has not yet certified peers.

  myPubKeyMB = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"
  udHistory = ""

  # Get the informations /ud/history/[pubkey] from the given node :
  # The history of ud
  # How to make the difference with /tx/history/[pubkey] ? ud.History
  def getUdHistory():
      global udHistory
      # Here we request for the path /ud/ "history/[pubkey]" through the "Basic Merkled API"
      udHistory = yield from ud.History(Endpoint.from_inline(myEndpoint).conn_handler(), myPubKey).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getUdHistory())

  print("\nudHistory :")
  print(udHistory)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/blockchain/block/[NUMBER]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#blockchainblocknumber

.. code-block:: python

  # ----------- GET the promoted block from the given number. -----------

  # Can generate an error on an empty blockchain, if the network has not yet certified peers.
  numberBlock = 3
  blockchainBlock = ""

  # Get the informations /blockchain/block/[NUMBER] from the given node :
  # Information on the given block on the blockchain.
  def getBlockchainBlock():
      global blockchainBlock
      # Here we request for the path /blockchain/ "block/[NUMBER]" through the "Basic Merkled API"
      blockchainBlock = yield from Block(Endpoint.from_inline(myEndpoint).conn_handler(), numberBlock).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getBlockchainBlock())

  print("blockchainBlock")
  print(blockchainBlock)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/tx/history/[PUBKEY]/blocks/[FROM]/[TO]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#txhistorypubkeyblocksfromto

.. code-block:: python

  # ----------- GET the promoted block from the given number.  -----------

  # Can generate an error on an empty blockchain, if the network has not yet certified peers.
  fromBlock = 1
  toBlock = 3
  txHistoryBlocks = ""

  # Get the informations /tx/history/[PUBKEY]/blocks/[FROM]/[TO] from the given node :
  # Information on the given block on the blockchain, with the given public key.
  def getTxHistoryBlocks():
      global txHistoryBlocks
      # Here we request for the path /tx/history/[PUBKEY]/blocks/[FROM]/[TO] through the "Basic Merkled API"
      txHistoryBlocks = yield from history.Blocks(Endpoint.from_inline(myEndpoint).conn_handler(), myPubKey, fromBlock, toBlock).get()

  # Call the asynchronous function :
  asyncio.get_event_loop().run_until_complete(getTxHistoryBlocks())

  print("\ntxHistoryBlocks")
  print(txHistoryBlocks)


\- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


``/tx/history/[PUBKEY]/times/[FROM]/[TO]`` :

https://github.com/ucoin-io/ucoin/blob/master/doc/HTTP_API.md#txhistorypubkeytimesfromto

.. code-block:: python

  # ----------- Get the wallet transaction history  -----------

  # Not yet implemented in the Python API : /tx/history/[PUBKEY]/times/[FROM]/[TO]
