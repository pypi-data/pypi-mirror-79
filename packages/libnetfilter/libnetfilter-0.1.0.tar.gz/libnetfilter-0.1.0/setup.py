# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libnetfilter',
 'libnetfilter.conntrack',
 'libnetfilter.log',
 'libnetfilter.netlink',
 'libnetfilter.queue']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libnetfilter',
    'version': '0.1.0',
    'description': 'Python wrapper (partial) around libnetfilter libraries',
    'long_description': "This package unashamedly pilfered from `commonism/python-libnetfilter`_. I've simple done a little reformatting and set it up to use `poetry`_.\n\n.. _commonism/python-libnetfilter: https://github.com/commonism/python-libnetfilter\n.. _poetry: https://python-poetry.org\n\n---------\n\nThis package wraps the ``netfilter`` ``C`` libraries:\n\n- libnetfilter_log_\n- libnetfilter_queue_\n- libnetfilter_conntrack_\n\n.. _libnetfilter_log: https://www.netfilter.org/projects/libnetfilter_log/index.html \n.. _libnetfilter_queue: https://www.netfilter.org/projects/libnetfilter_queue/index.html \n.. _libnetfilter_conntrack: https://www.netfilter.org/projects/libnetfilter_conntrack/index.html \n\nThese libraries need to be installed on your system before using this package.\n\nOn Debian: ``apt-get install libnetfilter-conntrack3 libnetfilter-log1 libnetfilter-queue1``\n",
    'author': 'Mark Bools',
    'author_email': 'mark@saltyvagrant.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/python-utils2/libnetfilter',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
