import argparse
import os
import sys
from .version import versionChecker
from .create import creator
from .release import release

"""wapttools.wapttools: provides entry point main()."""

__version__ = '1.1.0'


def main():
    parser = argparse.ArgumentParser(prog='wapttools', description='WAPT packaging utility.')
    subparsers = parser.add_subparsers(
        title='commands',
        dest='command')

    subparsers.add_parser(
        'version',
        help='display version')

    parser_check = subparsers.add_parser(
        'check-version',
        help='check if new upstream package exists')

    parser_check.add_argument(
        '--chat',
        help='send results to chat',
        action='store_true')

    parser_new = subparsers.add_parser(
        'new-package',
        help='create a new package')

    parser_new.add_argument(
        '--name',
        help='name of the new package to create',
        type=str)

    subparsers.add_parser(
        'release',
        help='release package to production')

    subparsers.add_parser(
        'git-flow',
        help='initialize git flow in current folder')

    parser.add_argument('--verbose', help='increase output verbosity', action='store_true')

    args = parser.parse_args()

    if args.command == 'version':
        print('wapttools cli v{}'.format(__version__))
        sys.exit(0)

    if args.command == 'check-version':
        mismatch = versionChecker(verbose=args.verbose, chat=args.chat)
        if mismatch:
            sys.exit(1)
        else:
            sys.exit(0)

    if args.command == 'new-package':
        creator(args.new_name, verbose=args.verbose)
        sys.exit(0)

    if args.command == 'release':
        release(os.path.basename(os.getcwd()), verbose=args.verbose)
        sys.exit(0)

    if args.command == 'git-flow':
        os.system('git flow init --defaults --force')
        sys.exit(0)
