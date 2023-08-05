import importlib.machinery
import importlib.util
import logging
import os
import shlex
import subprocess
import sys

logger = logging.getLogger(__name__)


class TrackSubClasses(type):
    """A metaclass that stores subclass name-to-class mappings in the base class"""

    @staticmethod
    def sorted_by_kind(cls):
        return [item for _, item in sorted((it.__kind__, it) for it in cls.__subclasses__.values())]

    def __init__(cls, name, bases, namespace):
        for base in bases:
            if base == object:
                continue

            for attr in ('__required__', '__optional__'):
                if not hasattr(base, attr):
                    continue

                inherited = getattr(base, attr, ())
                new_value = tuple(namespace.get(attr, ())) + tuple(inherited)
                namespace[attr] = new_value
                setattr(cls, attr, new_value)

        for base in bases:
            if base == object:
                continue

            if hasattr(cls, '__kind__'):
                subclasses = getattr(base, '__subclasses__', None)
                if subclasses is not None:
                    logger.info('Registering %r as %s', cls, cls.__kind__)
                    subclasses[cls.__kind__] = cls
                    break
            else:
                anonymous_subclasses = getattr(base, '__anonymous_subclasses__', None)
                if anonymous_subclasses is not None:
                    logger.info('Registering %r', cls)
                    anonymous_subclasses.append(cls)
                    break

        super().__init__(name, bases, namespace)


def atomic_rename(old_filename, new_filename):
    if os.name == 'nt' and os.path.exists(new_filename):
        new_old_filename = new_filename + '.bak'
        if os.path.exists(new_old_filename):
            os.remove(new_old_filename)
        os.rename(new_filename, new_old_filename)
        os.rename(old_filename, new_filename)
        if os.path.exists(new_old_filename):
            os.remove(new_old_filename)
    else:
        os.rename(old_filename, new_filename)


def edit_file(filename):
    editor = os.environ.get('EDITOR', None)
    if not editor:
        editor = os.environ.get('VISUAL', None)
    if not editor:
        raise SystemExit('Please set $VISUAL or $EDITOR.')

    subprocess.check_call(shlex.split(editor) + [filename])


def import_module_from_source(module_name, source_path):
    loader = importlib.machinery.SourceFileLoader(module_name, source_path)
    spec = importlib.util.spec_from_file_location(module_name, source_path, loader=loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    loader.exec_module(module)
    return module


def chunkstring(string, length, *, numbering=False):
    if len(string) <= length:
        return [string]

    if numbering:
        # Subtract to fit numbering (FIXME: this breaks for > 9 chunks)
        length -= len(' (0/0)')
        parts = []
        string = string.strip()
        while string:
            if len(string) <= length:
                parts.append(string)
                string = ''
                break

            idx = string.rfind(' ', 1, length + 1)
            if idx == -1:
                idx = string.rfind('\n', 1, length + 1)
            if idx == -1:
                idx = length
            parts.append(string[:idx])
            string = string[idx:].strip()
        return (f'{part} ({i + 1}/{len(parts)})' for i, part in enumerate(parts))

    return (string[i:length + i].strip() for i in range(0, len(string), length))
