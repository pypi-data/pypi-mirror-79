import datetime
import logging
import os
from .config import loadControl

log = logging.getLogger()


def release():
    """ Release package
    """
    control = loadControl()
    version_tag = '{version}-{datetag}'.format(
        version=control['version'],
        datetag=datetime.datetime.now().strftime('%Y%j.%H%M%S'))

    command = 'git flow release start v{tag}'.format(tag=version_tag)
    log.debug('* {}'.format(command))

    os.system(command)

    command = 'git flow release finish '
    command += '--push --pushtag --nopushdevelop --nokeep --force_delete '
    command += '--message "Release v{version} on {date}" v{tag}'
    command = command.format(
        tag=version_tag,
        version=control['version'],
        date=datetime.datetime.now().strftime('%Y-%m-%d, %H:%M'))
    log.debug('* {}'.format(command))

    os.system(command)
