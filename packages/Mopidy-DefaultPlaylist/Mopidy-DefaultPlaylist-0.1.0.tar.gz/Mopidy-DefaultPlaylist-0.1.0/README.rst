****************************
Mopidy-DefaultPlaylist
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-DefaultPlaylist
    :target: https://pypi.org/project/Mopidy-DefaultPlaylist/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/circleci/build/gh/michaelmeer/mopidy-defaultplaylist
    :target: https://circleci.com/gh/michaelmeer/mopidy-defaultplaylist
    :alt: CircleCI build status

.. image:: https://img.shields.io/codecov/c/gh/michaelmeer/mopidy-defaultplaylist
    :target: https://codecov.io/gh/michaelmeer/mopidy-defaultplaylist
    :alt: Test coverage

Sets a default playlist for Mopidy, and allows to start playing it automatically after start of the Mopidy service. Optionally allows to set shuffle mode on. This can be useful for projects like the `Pimoroni Pirate Radio <https://learn.pimoroni.com/tutorial/sandyj/streaming-spotify-to-your-pi/>`_.


Installation
============

Install by running::

    python3 -m pip install Mopidy-DefaultPlaylist

See https://mopidy.com/ext/defaultplaylist/ for alternative installation methods.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-DefaultPlaylist to your Mopidy configuration file::

    [defaultplaylist]
    enabled = true
    defaultplaylist_name = Top Hits
    autoplay = true
    shuffle = true

The default


Project resources
=================

- `Source code <https://github.com/michaelmeer/mopidy-defaultplaylist>`_
- `Issue tracker <https://github.com/michaelmeer/mopidy-defaultplaylist/issues>`_
- `Changelog <https://github.com/michaelmeer/mopidy-defaultplaylist/blob/master/CHANGELOG.rst>`_


Credits
=======

- Original author: `Michael Meer <https://github.com/michaelmeer>`__
- Current maintainer: `Michael Meer <https://github.com/michaelmeer>`__
- `Contributors <https://github.com/michaelmeer/mopidy-defaultplaylist/graphs/contributors>`_
