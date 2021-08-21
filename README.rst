python-mapc2020
===============

An experimental Python client for the 2020/21 edition of the Multi-Agent
Programming Contest. Used in our WESAAC 2021 short course.

Install
-------

.. code::

    pip install git+https://github.com/agentcontest/python-mapc2020

Example
-------

.. code:: python

    >>> import mapc2020
    >>> agent = mapc2020.Agent.open("agentA1", "1")

    >>> agent.move("n")

.. image:: example.svg
    :alt: <Agent view>

Missing features
----------------

This library may be useful to experiment, but probably not suitable for
participating in the contest just yet. It currently does not handle:

* Simulation changes
* Reestablishing interrupted connections
* In-depth type-checking of percepts and messages
