
__all__ = ()

# python
from argparse import ArgumentParser
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Optional, Sequence
# aw11
from .version import __version__


__directory__ = os.path.abspath(os.path.dirname(__file__))


def main(args: Sequence[str] = None) -> None:
    argparser = create_argparser()
    args = argparser.parse_args(args)

    if args.version:
        sys.stdout.write(f'{get_version()}\n')
        return

    clean([Path(fp) for fp in args.file_paths], dry=args.dry)


TRAILING_WHITESPACE_PATTERN = re.compile(r'[ \t]+$', re.MULTILINE)
PYTHON_DOCSTRING_PATTERN = re.compile('^("""|\'\'\')')


def remove_trailing_whitespace(file_contents: str) -> str:
    return TRAILING_WHITESPACE_PATTERN.sub('', file_contents)


def ensure_starting_newline(file_contents: str) -> str:
    # don't mess with interpreter directives
    if file_contents.startswith('#!'):
        return file_contents
    # don't mess with python module docstrings
    if PYTHON_DOCSTRING_PATTERN.match(file_contents):
        return file_contents

    return '\n' + file_contents.lstrip('\n')


def ensure_trailing_newline(file_contents: str) -> str:
    return file_contents.rstrip('\n') + '\n'


def clean(file_paths: Sequence[Path], *, dry: bool = False) -> None:
    for file_path in file_paths:
        # convert the the file path to be relative to the cwd
        try:
            file_path = file_path.resolve().relative_to(Path('.').resolve())
        except Exception:
            sys.stderr.write(f'{file_path} not found')
            continue

        try:
            with open(file_path, encoding='utf8') as file:
                modified_file_contents = original_file_contents = file.read()
        except UnicodeDecodeError:
            continue

        modified_file_contents = remove_trailing_whitespace(
            modified_file_contents,
        )
        modified_file_contents = ensure_trailing_newline(
            modified_file_contents,
        )
        modified_file_contents = ensure_starting_newline(
            modified_file_contents,
        )

        if not dry:
            if modified_file_contents != original_file_contents:
                sys.stdout.write(f'{file_path}\n')
                with open(file_path, 'w') as file:
                    file.write(modified_file_contents)


def get_version() -> str:
    if not __version__.endswith('.dev'):
        return __version__

    commit_hash: Optional[str]
    try:
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            stderr=subprocess.DEVNULL,
            cwd=__directory__,
        ).decode('utf8').strip()
    except Exception:
        commit_hash = None

    try:
        is_dirty = bool(subprocess.check_output(
            ['git', 'status', '-u', 'no', '--porcelain'],
            stderr=subprocess.DEVNULL,
            cwd=__directory__,
        ))
    except Exception:
        is_dirty = False

    local_version = ''
    if commit_hash is not None:
        local_version += commit_hash
    if is_dirty:
        local_version += '.dirty'

    if local_version:
        return f'{__version__}[+{local_version}]'
    return __version__


def create_argparser() -> ArgumentParser:
    argparser = ArgumentParser(
        description='A general code and config formatter. '
                    'Removes trailing whitespace. '
                    'Ensures a starting and trailing newline.',
    )
    argparser.add_argument(
        'file_paths',
        metavar='filepath',
        nargs='*',
        help='the files to format',
    )
    argparser.add_argument(
        '--dry',
        dest='dry',
        action='store_true',
        help='tell if a file would be changed, but do not actually change it',
    )
    argparser.add_argument(
        '--version',
        dest='version',
        action='store_true',
        help='show version and exit',
    )
    return argparser


if __name__ == '__main__':
    main()
