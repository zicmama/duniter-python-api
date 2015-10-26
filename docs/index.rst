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
      # You can use either a complete defined endpoint : [NAME_OF_THE_API] [DOMAIN] [IPv4] [IPv6] [PORT]
      # or the simple definition : [NAME_OF_THE_API] [DOMAIN] [PORT]
      myEndpoint = "BASIC_MERKLED_API metab.ucoin.io 9201"

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

   how_to_use_the_api_get
   how_to_use_the_api_post
   documents
   key
   bma


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
