.. ucoinpy documentation master file, created by
   sphinx-quickstart on Tue Oct  6 16:34:46 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ucoinpy : A python implementation of uCoin API
==============================================

ucoinpy is a library to develop an application for uCoin.
ucoinpy helps to handle the following problem :

* Request Basic Merkle API provided by uCoin nodes
* Request nodes in a non-blocking way
* Handle uCoin signing keys


Library Installation
----------------------

.. code-block:: python

  $ pip install ucoinpy


Getting Started
----------------

Client example::

  import asyncio
  import aiohttp
  import ucoinpy

  # Get the information /node/summary from the given node :
  def getSummaryInfo():
      # The given node : [NAME_OF_THE_API] [DOMAIN] [IPV4] [IPV6] PORT]
      myEndpoint = "BASIC_MERKLED_API sbhosting.me 51.254.203.24 fe80::f816:3eff:fe79:c9af 8999"

      # or the Given node : [NAME_OF_THE_API] [DOMAIN] [PORT]
      myEndpoint = "BASIC_MERKLED_API sbhosting.me 8999"

      # Here we request for the path /node/ "summary" through the "Basic Merkled API"
      summaryInfo = yield from Summary(Endpoint.from_inline(myEndpoint).conn_handler()).get()

      print(summaryInfo)

  # Latest uCoin-Python-API is asynchronous and you have to use asyncio, an asyncio loop and a "yield from" on the data.
  # ( https://docs.python.org/3/library/asyncio.html )
  asyncio.get_event_loop().run_until_complete(getSummaryInfo())


Source code
-----------


.. image:: https://travis-ci.org/ucoin-io/ucoin-python-api.svg?branch=master
   :alt: Travis - Build's status of the project.


Sources can be found at https://github.com/ucoin-io/ucoin-python-api

Contributions are welcome.


Contents:
=========

.. toctree::
   :maxdepth: 2

   documents
   key
   bma
   how_to_use_the_api_get
   how_to_use_the_api_post


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
