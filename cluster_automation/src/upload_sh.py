""" Uploads the shell scripts used by robotron. """

import subprocess
from subprocess import PIPE, STDOUT
from os import path

import shlex

from robotron import get_user_host


def upload():
    """ Upload """
    (user, host) = get_user_host()
    source = path.join('..', 'sh', '*')
    remote = f"/home/{user}/scratch/tmp/hemispheric_PET/"
    target = f"{user}@{host}:{remote}"
    sshp = "/usr/bin/sshpass -f /home/cris/.ssh/ovgu-cluster-pass"
    rsyn = f"rsync --chmod=ug+rwx -av -e ssh {source} {target}"
    commandline = f"{sshp} {rsyn}"
    #print(commandline)
    commandline = shlex.split(commandline)
    #print(commandline)

    try:
        result = subprocess.run(commandline, stdout=PIPE, stderr=STDOUT,
                                universal_newlines=True, check=True, timeout=15)
    except subprocess.CalledProcessError as err:
        # Process ran but returned non-zero. If excepted, handle here.
        print(err.returncode)
        raise
    return result.stdout


if __name__ == "__main__":
    print(upload())
