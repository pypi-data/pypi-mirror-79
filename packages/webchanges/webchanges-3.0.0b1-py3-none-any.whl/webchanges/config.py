import argparse
import os.path

import webchanges as project


class BaseConfig(object):

    def __init__(self, project_name, config_dir, config, jobs, cache, hooks, verbose):
        self.project_name = project_name
        self.config_dir = config_dir
        self.config = config
        self.jobs = jobs
        self.cache = cache
        self.hooks = hooks
        self.verbose = verbose


class CommandConfig(BaseConfig):

    def __init__(self, project_name, config_dir, bindir, prefix, config, jobs, hooks, cache, verbose):
        super().__init__(project_name, config_dir, config, jobs, cache, hooks, verbose)
        self.bindir = bindir
        self.prefix = prefix

        if self.bindir == 'bin':
            # Installed system-wide
            self.examples_dir = os.path.join(prefix, 'share', self.project_name, 'examples')
        else:
            # Assume we are not yet installed
            self.examples_dir = os.path.join(prefix, bindir, 'share', self.project_name, 'examples')

        self.urls_yaml_example = os.path.join(self.examples_dir, 'jobs-example.yaml')
        self.hooks_py_example = os.path.join(self.examples_dir, 'hooks-example.py')

        self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(description=project.__doc__,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('--version', action='version', version=f'{project.__project_name__} {project.__version__}')
        parser.add_argument('-v', '--verbose', action='store_true', help='show debug output')
        group = parser.add_argument_group('files and directories')
        group.add_argument('--jobs', '--urls', dest='jobs', metavar='FILE',
                           help='read job list (URLs) from FILE', default=self.jobs)
        group.add_argument('--config', metavar='FILE', help='read configuration from FILE', default=self.config)
        group.add_argument('--hooks', metavar='FILE', help='use FILE as hooks.py module', default=self.hooks)
        group.add_argument('--cache', metavar='FILE', help=('use FILE as cache database, '
                                                            'alternatively can accept a redis URI'), default=self.cache)
        group = parser.add_argument_group('job list management')
        group.add_argument('--list', action='store_true', help='list jobs')
        group.add_argument('--add', metavar='JOB', help='add job (key1=value1,key2=value2,...)')
        group.add_argument('--delete', metavar='JOB', help='delete job by location or index')
        group.add_argument('--test', '--test-filter', dest='test_filter', metavar='JOB',
                           help='test filter output of job by location or index')
        group.add_argument('--test-diff', '--test-diff-filter', dest='test_diff_filter', metavar='JOB',
                           help='test diff filter output of job by location or index (needs at least 2 snapshots)')
        group = parser.add_argument_group('Authentication')
        group.add_argument('--smtp-login', action='store_true', help='Check SMTP login')
        group.add_argument('--telegram-chats', action='store_true', help='List telegram chats the bot is joined to')
        group.add_argument('--test-reporter', metavar='REPORTER', help='Send a test notification')
        group.add_argument('--xmpp-login', action='store_true', help='Enter password for XMPP (store in keyring)')

        group = parser.add_argument_group('interactive commands ($EDITOR/$VISUAL)')
        group.add_argument('--edit', action='store_true', help='edit URL/job list')
        group.add_argument('--edit-config', action='store_true', help='edit configuration file')
        group.add_argument('--edit-hooks', action='store_true', help='edit hooks script')
        group = parser.add_argument_group('miscellaneous')
        group.add_argument('--features', action='store_true', help='list supported jobs/filters/reporters')
        group.add_argument('--gc-cache', action='store_true', help='remove old cache entries (snapshots)')

        args = parser.parse_args()

        for i, arg in enumerate(vars(args)):
            argval = getattr(args, arg)
            setattr(self, arg, argval)

        return parser
