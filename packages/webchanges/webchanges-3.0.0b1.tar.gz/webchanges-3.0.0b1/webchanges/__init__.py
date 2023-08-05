"""webchanges monitors webpages for you

webchanges is intended to help you watch changes in webpages and get notified (via e-mail, in your terminal or through
various third party services) of any changes. The change notification will include the URL that has changed and a
unified diff of what has changed.
"""

__project_name__ = __package__
__version__ = '3.0.0b1'  # use pkg_resources.parse_version to parse
__min_python_version__ = (3, 6)
__author__ = 'Mike Borsetti <mike@borsetti.com>'
__copyright__ = 'Copyright 2020- Mike Borsetti'
__license__ = 'MIT, BSD 3-Clause License'
__url__ = f'https://github.com/mborsetti/{__package__}'
__user_agent__ = f'{__name__}/{__version__} (+{__url__})'

def init_data():
    return {k: v for k, v in globals().items()}