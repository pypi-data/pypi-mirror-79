#!/usr/bin/env python3

"""This is the main program"""

import logging
import os.path
import signal
import sys

from appdirs import AppDirs

# Check if we are installed in the system already
(prefix, bindir) = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
if bindir != 'bin':
    sys.path.insert(1, os.path.dirname(os.path.abspath(sys.argv[0])))

sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__))))


from .command import UrlwatchCommand  # noqa:E402 Module level import not at top of file
from .config import CommandConfig  # noqa:E402 Module level import not at top of file
from .main import Urlwatch  # noqa:E402 Module level import not at top of file
from .storage import CacheMiniDBStorage, CacheRedisStorage, JobsYaml, YamlConfigStorage  # noqa:E402 not top of file

project_name = __package__

# directory where the config, jobs and hooks files are located
if os.name != 'nt':
    config_dir = os.path.expanduser(os.path.join('~', '.' + project_name))
else:
    config_dir = os.path.expanduser(os.path.join('~', 'Documents', project_name))
if not os.path.exists(config_dir):
    config_dir = AppDirs(project_name).user_config_dir

# directory where the database is located
cache_dir = AppDirs(project_name).user_cache_dir

# Ignore SIGPIPE for stdout (see https://github.com/thp/urlwatch/issues/77)
try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except AttributeError:
    # Windows does not have signal.SIGPIPE
    ...

logger = logging.getLogger(project_name)




def setup_logger(verbose):
    if verbose:
        root_logger = logging.getLogger('')
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter('%(asctime)s %(module)s %(levelname)s: %(message)s'))
        root_logger.addHandler(console)
        root_logger.setLevel(logging.DEBUG)
        root_logger.info('turning on verbose logging mode')


def migrate_urlwatch_files(config_file, jobs_file, hooks_file):
    # migration from urlwatch 2.2
    if os.name != 'nt':
        urlwatch_dir = os.path.expanduser(os.path.join('~', '.' + 'urlwatch'))
    else:
        urlwatch_dir = os.path.expanduser(os.path.join('~', 'Documents', 'urlwatch'))
    if not os.path.exists(urlwatch_dir):
        urlwatch_dir = AppDirs('urlwatch').user_config_dir
    urlwatch_config_file = os.path.join(urlwatch_dir, 'urlwatch.yaml')
    urlwatch_urls_file = os.path.join(urlwatch_dir, 'urls.yaml')
    urlwatch_hooks_file = os.path.join(urlwatch_dir, 'hooks.py')
    for old_file, new_file in zip((urlwatch_config_file, urlwatch_urls_file, urlwatch_hooks_file),
                                  (config_file, jobs_file, hooks_file)):
        if old_file and not new_file:
            import shutil

            os.makedirs(os.path.dirname(new_file), exist_ok=True)
            shutil.copyfile(old_file, new_file)
            logger.warning(f'Copied urlwatch {old_file} to {project_name} {new_file}')


def main():
    # The config, jobs and hooks files
    config_file = os.path.join(config_dir, 'config.yaml')
    jobs_file = os.path.join(config_dir, 'jobs.yaml')
    hooks_file = os.path.join(config_dir, 'hooks.py')
    cache_file = os.path.join(cache_dir, 'cache.db')

    # migrate legacy urlwatch 2.2 files
    migrate_urlwatch_files(config_file, jobs_file, hooks_file)

    # load config files
    command_config = CommandConfig(project_name, config_dir, bindir, prefix, config_file, jobs_file, hooks_file,
                                   cache_file, verbose=False)
    setup_logger(command_config.verbose)

    # setup storage API
    config_storage = YamlConfigStorage(command_config.config)

    if any(command_config.cache.startswith(prefix) for prefix in ('redis://', 'rediss://')):
        cache_storage = CacheRedisStorage(command_config.cache)
    else:
        cache_storage = CacheMiniDBStorage(command_config.cache)

    jobs_storage = JobsYaml(command_config.jobs)

    # setup urlwatch
    urlwatch = Urlwatch(command_config, config_storage, cache_storage, jobs_storage)
    urlwatch_command = UrlwatchCommand(urlwatch)

    # run urlwatch
    urlwatch_command.run()


if __name__ == '__main__':
    main()


# to be used by argparse-manpage as below (issue: attempted relative import with no known parent package)
def manpage_parser():
    return CommandConfig(project_name, config_dir, bindir, prefix, '', '', '', '',
                         verbose=False).parse_args()

# from build_manpages.manpage import Manpage
# print(Manpage(manpage_parser()))
