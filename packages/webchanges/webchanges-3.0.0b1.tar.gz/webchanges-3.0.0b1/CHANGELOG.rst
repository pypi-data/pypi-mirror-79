The format mostly follows `Keep a Changelog <http://keepachangelog.com/en/1.0.0/>`__

Version 3.0.0 (2020-09-15)
==========================

Milestone
---------
Initial release of `webchanges` as an updated fork of `urlwatch` 2.2.

Below is a summary of the changes introduced from `urlwatch` 2.2

Features
--------
* Backward compatible with `urlwatch` 2.2
* You can now specify just the ``url`` in the job file and defaults are set for you. "Just works" philosophy optimizes
  the monitoring of text in webpages and all necessary filters are applied.
* The Python ``html2text`` package (used by the ``html2text`` filter, previously known as ``pyhtml2text``) is now
  initialized with the following settings: **XXXX**
* If no ``name`` is provided, the title of an HTML page will be used for a job name.
* The output from ``html2text`` filter is reconstructed into HTML for html reports, which now include clickable
  inline links, basic formatting is also preserved (lists, bolding, italics, etc.)
* HTML reports are rendered correctly by email clients and their formatting has been made radically more legible and
  useful, including lines wrap around
* New ``additions_only`` and ``deletions_only`` report filters allow you to only track content that was added (or
  deleted) from the source.

Changes and deprecations
-------------------------
* Navigation by full browser is now accomplished by specifying the ``url`` and setting ``use_browser: true``.
  The key ``navigate`` has been deprecated for clarity.
* The name of the default job's configuration file has been changed to ``jobs.yaml``. If at launch ``urls.yaml`` is
  found at startup, it is copied over for backward-compatibility).
* The location of config files in Windows has been moved to ``%USERPROFILE%/Documents/urlwatch``
  where they can be more easily edited and backed up.
* The ``html2text`` filter defaults to using the Python ``html2text`` package (with optimized defaults).
* New `additions_only` key to report only added lines (useful when monitoring only new content)
* New `deletions_only` key to report only deleted lines
* `keyring` and `cssselect` Python packages are no longer installed by default
* The ``html2text`` filter's ``re`` method has been renamed ``strip_tags``, which is deprecated and will trigger a
  warning.
* The ``html2text`` filter's ``lynx`` method is no longer supported. Use ``html2text`` instead.
* The ``grep`` filter has been renamed ``keep_lines_matching``, which is deprecated and will trigger a warning.
* The ``grepi`` filter has been renamed ``delete_lines_matching``, which is deprecated and will trigger a warning.
* ``--test`` command line is used to test a job (formerly ``--test-filter``, deprecated and will trigger a warning).
* ``--test-diff`` command line is used to test a jobs' diff (formerly ``--test-diff-filter``, deprecated and will
  trigger a warning).
* The key ``kind`` has been deprecated (but is still used internally).
* The database (cache) file is backed up at every run to `*.bak`
* The list of default and optional dependencies has been updated (see documentation) to enable "Just works"
* Dependencies are now sepecified as PyPi `extras
  <https://stackoverflow.com/questions/52474931/what-is-extra-in-pypi-dependency>`__ and can be installed with
  `webchanges`

Bugfixes
--------

* The ``html2text`` filter's ``html2text`` method defaults to unicode handling
* HTML href html links ending with spaces are no longer broken by the spaces being replaced with `%20` by ``xpath``
* No longer sorts keys alphabetically when writing a config file (e.g. for the first time)

Tests
-----

* Added flake8 to the test suite

Documentation changes
---------------------

* Complete rewrite

Misc
----

* Added support for Python 3.9
