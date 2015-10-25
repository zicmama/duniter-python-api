#### How to use the Python uCoin API to Get a specified data

.. code-block:: python

  import aiohttp, asyncio, ucoinpy

  # You can use either complete format endpoint with IPV4 or with IPV6 ; or either the format : domain name + port.

  # Given node : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] PORT]
  #myEndpoint = "BASIC_MERKLED_API sbhosting.me 51.254.203.24 fe80::f816:3eff:fe79:c9af 8999"
  # Given node : [NAME_OF_THE_API] [DOMAIN] [PORT]
  myEndpoint = "BASIC_MERKLED_API metab.ucoin.io 9201"

  myPubKeyMB = "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk"

<br />

--------------------

<br />

.. code-block:: python

  # ----- Display general info on the currency network -----------

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

<br />

--------------------

<br />

.. code-block:: python
  # ----- Display general info on the currency network -----------

  blockchainParameters = ""

  # Get the informations /blockchain/parameters from the given node :
  # Information of the blockchain or currency
  def getBlockchainParameters():
      global blockchainParameters
      # Here we request for the path /blockchain/ "parameters" through the "Basic Merkled API"
      blockchainParameters = yield from Parameters(Endpoint.from_inline(myEndpoint).conn_handler()).get()

  asyncio.get_event_loop().run_until_complete(getBlockchainParameters())

  # ----- Display general info on the currency network -----------
  # Call the asynchronous function :
  print("\nblockchainParameters :")
  print(blockchainParameters)

  <br />

  --------------------

  <br />

.. code-block:: python
    # ----- Display general info on the currency network -----------
