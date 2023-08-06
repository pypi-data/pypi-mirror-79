# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['packet_trace']

package_data = \
{'': ['*']}

install_requires = \
['libnetfilter>=0.1.0,<0.2.0', 'python-iptables>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['ptrace = packet_trace.main:main']}

setup_kwargs = {
    'name': 'packet-trace',
    'version': '0.1a0',
    'description': 'A simple tool to trace packets as they pass through Linux netfilter.',
    'long_description': 'This code pilfered from `commonism/iptables-trace`_ with some reformatting and modification to form suitable to `poetry`_.\n\n.. _commonism/iptables-trace: https://github.com/commonism/iptables-trace\n.. _poetry: https://python-poetry.org\n\n--------\n\nInstallation\n------------\n\nBefore using this script install the libnetfilter_ package (if you use ``poetry install`` this willl be done automatically using the latest ``gitlab.com`` code).\n\n.. _libnetfilter: https://gitlab.com/python-utils2/libnetfilter\n\nUsage\n-----\n\nThis script adds ``TRACE`` rules into ``nftables`` and then analyses the resulting log output to present its results, consequently it must be run as a privileged user (one permitted to modify the ``nftables``).\n',
    'author': 'Mark Bools',
    'author_email': 'mark@saltyvagrant.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/python-utils2/packet_trace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
