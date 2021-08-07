python-mapc2020
===============

An experimental Python client for the 2020/21 edition of the Multi-Agent
Programming Contest.

Install
-------

.. code::

    pip install git+https://github.com/agentcontest/python-mapc2020

Example
-------

.. code:: python

    >>> agent = mapc2020.Agent.open("agentA1", "1")

    >>> agent.move("n")

.. image:: example.svg
    :alt: <Agent view>

Todo
----

* [ ] Testing

Stretch goals
-------------
* [ ] Seamless reconnects
* [ ] Seamless simulation change
* [ ] In-depth typing
* [ ] Provide more documentation
