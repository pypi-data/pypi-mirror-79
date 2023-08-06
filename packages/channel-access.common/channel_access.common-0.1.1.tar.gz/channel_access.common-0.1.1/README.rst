Channel Access common library
=============================
This library contains the low-level bindings to the common channel access
constants and common utility functions.

This is a support library used by `channel_access.client`_ and `channel_access.server`_.

.. _channel_access.client: https://pypi.org/project/channel_access.client
.. _channel_access.server: https://pypi.org/project/channel_access.server

Installation
------------
Before installing the library, the environment variables ``EPICS_BASE``
and ``EPICS_HOST_ARCH`` must be set.

Then the library can be installed with pip::

    pip install channel_access.common

Documentation
-------------
The documentation is available `online`_ or it can be
generated from the source code with *sphinx*::

    cd /path/to/repository
    pip install -e .
    python setup.py build_sphinx

Then open ``build/sphinx/html/index.html``.

.. _online: https://delta-accelerator.github.io/channel_access.common

Get the source
--------------
The source code is available in a `Github repository`_::

    git clone https://github.com/delta-accelerator/channel_access.common

.. _Github repository: https://github.com/delta-accelerator/channel_access.common

Tests
-----
Tests are run with *pytest*::

    cd /path/to/repository
    pytest -v

To run the tests for all supported version use *tox*::

    cd /path/to/repository
    tox
