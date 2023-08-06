import datetime
import logging
import os
import subprocess
from .config import loadControl

log = logging.getLogger()


def release():
    """ Release package
    """
    control = loadControl()
    hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
    tag = 'v{}-{}'.format(control['version'], hash)

    command = 'git flow release start {tag}'.format(tag=tag)
    log.debug('{}'.format(command))
    os.system(command)

    command = 'git flow release finish '
    command += '--push --pushtag --nokeep --force_delete '
    command += '--message "Release v{version} ({hash}) on {date}" {tag}'
    command = command.format(
        tag=tag,
        hash=hash,
        version=control['version'],
        date=datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S'))
    log.debug('{}'.format(command))
    os.system(command)
