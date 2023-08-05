.. _reports:

=======
Reports
=======

Reports are the text of the summary, and can be one of the following formats (depending on what
ref:`reporter <reporters>` you use):

* :ref:`text`
* :ref:`html`
* :ref:`markdown`

.. _text:

Text
----
Unicode text.

**Optional sub-directives**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* minimal: An abbreviated version (directives below are ignored)
* line_length: The maximum length of each line
* show_details: Show details of each job
* show_footer: Show footer listing number of jobs and elapsed time


.. _html:

HTML
----
HTML.

These reports are by default ``unified`` diffs that are prettified by `webchanges`.

If for some reason you want the output to be the python `HtmlDiff
<https://docs.python.org/3/library/difflib.html#difflib.HtmlDiff>`__ table format, set the sub-directive ``diff`` to
``table``.

**Optional sub-directives**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* diff: unified (default) or table. See above.


.. _markdown:

Markdown
--------
Markdown text, used for Matrix.

**Optional sub-directives**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* minimal: An abbreviated version (directives below are ignored)
* show_details: Show details of each job
* show_footer: Show footer listing number of jobs and elapsed time
