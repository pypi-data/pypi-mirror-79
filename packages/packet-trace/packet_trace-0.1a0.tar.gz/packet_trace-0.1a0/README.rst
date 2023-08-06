This code pilfered from `commonism/iptables-trace`_ with some reformatting and modification to form suitable to `poetry`_.

.. _commonism/iptables-trace: https://github.com/commonism/iptables-trace
.. _poetry: https://python-poetry.org

--------

Installation
------------

Before using this script install the libnetfilter_ package (if you use ``poetry install`` this willl be done automatically using the latest ``gitlab.com`` code).

.. _libnetfilter: https://gitlab.com/python-utils2/libnetfilter

Usage
-----

This script adds ``TRACE`` rules into ``nftables`` and then analyses the resulting log output to present its results, consequently it must be run as a privileged user (one permitted to modify the ``nftables``).
