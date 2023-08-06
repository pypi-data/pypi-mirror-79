import argparse
import logging
import os
import sys
from .vers import __version__
from .check import isPackage
from .version import versionChecker
from .validate import validate
from .create import create
from .build import build
from .release import release

log = logging.getLogger()


def cli():
    parser = argparse.ArgumentParser(prog='wapt', description='WAPT packaging utility.')
    subparsers = parser.add_subparsers(
        title='commands',
        dest='command')

    subparsers.add_parser(
        'version',
        help='display cli version')

    parser_check = subparsers.add_parser(
        'check-version',
        help='check if new upstream package exists')

    parser_check.add_argument(
        '--chat',
        help='send results to chat',
        action='store_true')

    parser_check.add_argument(
        '--badge',
        help='generate badge',
        action='store_true')

    subparsers.add_parser(
        'validate',
        help='validate package')

    parser_new = subparsers.add_parser(
        'create',
        help='create a new package')

    parser_new.add_argument(
        '--name',
        help='name of the new package to create',
        type=str)

    subparsers.add_parser(
        'build',
        help='build package from current folder')

    parser_upload = subparsers.add_parser(
        'upload',
        help='upload package')

    parser_upload.add_argument(
        '--server',
        help='WAPT server url',
        type=str)

    parser_upload.add_argument(
        '--key',
        help='key path to sign package',
        type=str)

    parser_upload.add_argument(
        '--user',
        help='WAPT server url',
        type=str)

    subparsers.add_parser(
        'release',
        help='release package to production')

    subparsers.add_parser(
        'setup',
        help='initialize folder after git clone')

    parser.add_argument('--verbose', help='verbose output', action='store_true')
    parser.add_argument('--silent', help='no output except critical messages', action='store_true')

    args = parser.parse_args()

    logging_config = logging.StreamHandler(sys.stdout)
    logging_config.setFormatter(logging.Formatter('[%(asctime)s - %(levelname)8s] %(message)s'))
    log.addHandler(logging_config)

    if args.silent:
        log.setLevel(logging.CRITICAL)
    elif args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    if args.command == 'version':
        log.info('WAPT Tools CLI v{}'.format(__version__))
        sys.exit(0)

    if args.command == 'check-version':
        log.info('WAPT Tools CLI v{}'.format(__version__))
        if not isPackage():
            sys.exit(1)

        mismatch = versionChecker(chat=args.chat, badge=args.badge)
        if mismatch:
            sys.exit(1)
        else:
            sys.exit(0)

    if args.command == 'validate':
        log.info('WAPT Tools CLI v{}'.format(__version__))
        if not isPackage():
            sys.exit(1)

        if not validate():
            log.error('not a valid package')
            sys.exit(1)
        else:
            log.info('valid package')
            sys.exit(0)

    if args.command == 'create':
        log.info('WAPT Tools CLI v{}'.format(__version__))
        create(args.name)
        sys.exit(0)

    if args.command == 'build':
        log.info('WAPT Tools CLI v{}'.format(__version__))
        if not isPackage():
            sys.exit(1)

        build()
        sys.exit(0)

    if args.command == 'release':
        log.info('WAPT Tools CLI v{}'.format(__version__))
        if not isPackage():
            sys.exit(1)

        release()
        sys.exit(0)

    if args.command == 'setup':
        log.info('WAPT Tools CLI v{}'.format(__version__))
        if not isPackage():
            sys.exit(1)

        os.system('git flow init --defaults --force')
        sys.exit(0)
