This package unashamedly pilfered from `commonism/python-libnetfilter`_. I've simple done a little reformatting and set it up to use `poetry`_.

.. _commonism/python-libnetfilter: https://github.com/commonism/python-libnetfilter
.. _poetry: https://python-poetry.org

---------

This package wraps the ``netfilter`` ``C`` libraries:

- libnetfilter_log_
- libnetfilter_queue_
- libnetfilter_conntrack_

.. _libnetfilter_log: https://www.netfilter.org/projects/libnetfilter_log/index.html 
.. _libnetfilter_queue: https://www.netfilter.org/projects/libnetfilter_queue/index.html 
.. _libnetfilter_conntrack: https://www.netfilter.org/projects/libnetfilter_conntrack/index.html 

These libraries need to be installed on your system before using this package.

On Debian: ``apt-get install libnetfilter-conntrack3 libnetfilter-log1 libnetfilter-queue1``
