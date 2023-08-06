import fnmatch
import json
import logging
import re
import os
from .control import controlCheck

log = logging.getLogger()


def validate():
    """ Validate a package
    """
    # Validate *.json files
    for root, _, files in os.walk('.'):
        for file in fnmatch.filter(files, '*.json'):
            path = os.path.join(root, file)
            log.debug('Validating json file {}'.format(path))
            with open(path, 'r') as json_file:
                try:
                    json.load(json_file)
                except ValueError:
                    log.error('{} is not a valid json file'.format(path))
                    return False

    # Validate WAPT/control file
    if not controlCheck():
        return False

    log.debug('Check for WAPT/icon.png')
    if not os.path.exists(os.path.join('WAPT', 'icon.png')):
        log.error('WAPT/icon.png missing')
        return False

    # Validate setup.py
    ok = {
        'def_install': False,
        'def_uninstall': False,
        'def_session_setup': False,
        'def_audit': False,
        'def_update_package': False,
        'def_dowload_sources': False,
        'commands': False,
    }
    with open('setup.py', 'r') as file:
        for line in file:
            if line[-2:] == '\r\n':
                log.error('Found CRLF in setup.py')
                return False

            if re.match('^def install(', line):
                ok['def_install'] = True
            elif re.match('^def uninstall(', line):
                ok['def_uninstall'] = True
            elif re.match('^def session_setup(', line):
                ok['def_session_setup'] = True
            elif re.match('^def audit(', line):
                ok['def_audit'] = True
            elif re.match('^def update_package(', line):
                ok['def_update_package'] = True
            elif re.match('^def dowload_sources(', line):
                ok['def_dowload_sources'] = True
            elif re.match('wapttools.commands(', line):
                ok['commands'] = True

    check = True
    for key in ok.keys():
        if not ok[key]:
            log.error('{} not found in setup.py'.format(key))
        check &= ok[key]

    return check
