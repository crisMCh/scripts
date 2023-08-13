""" Automation script for running and retrieving work on the Uni computing cluster.

The script needs to run on a machine with ssh access to the cluster (through VPN).
Takes a list with an arbitrary number of tuples (target_folder, macfile) to be 
processed sequentially.
"""

import time
import subprocess
from subprocess import PIPE, STDOUT
import argparse
import shlex

def main(worklist):
    """ Main """
    print("\nRobotron awakes! Found these tasks:")
    for (target_folder, mac_file) in worklist:
        print(f"Target: {target_folder : <26} Macro: {mac_file}")

    for (target_folder, mac_file) in worklist:
        print(f"\nWorking on: {target_folder}")

        #continue
        #upload_to_remote()
        #prepare_work()
        start_numbercrunching(target_folder, mac_file)
        wait_for_numbercrunching()
        finalize_work(target_folder, mac_file)
        wait_for_numbercrunching()
        download_from_remote(target_folder)


def debug(f_n):
    """ Debug decorator."""
    def wrapper(*args, **kwargs):
        print(f"Invoking {f_n.__name__}")
        print(f"  args: {args}")
        print(f"  kwargs: {kwargs}")
        result = f_n(*args, **kwargs)
        print(f"  returned {result}")
        return result
    return wrapper


def wait_for_numbercrunching(timeout=24 * 60 * 60):
    """ Sleeps until the queue has finished. Raises TimeoutError on timeout."""
    poll_interval = 1       # in seconds .. slow down adequately
    while not my_queue_isempty():
        timeout -= poll_interval
        if timeout > 0:
            print("Still waiting")
            time.sleep(poll_interval)
        else:
            raise TimeoutError("Timed out waiting for queue to finish")


def my_queue_isempty():
    """ Parses the queue status to check if the queue is finished."""
    queue_status = get_queue_status()
    (user, _) = get_user_host()

    # As long as our username appears in the queue we assume our work is not done yet.
    # This check could be improved by looking for specific job IDs for cases
    # when the user may be running other work from outside this script instance.
    if user in queue_status:
        empty = False
    # Test that at least some expected string was returned (e.g. table header)
    elif "JOBID" in queue_status:
        empty = True
    else:
        raise ValueError("Unexpected queue status response")
    return empty


def get_queue_status():
    """ Runs a command to get the current queue status."""
    command = "/usr/bin/squeue -u $USER"
    commandline = wrap_in_ssh(command)

    try:
        result = subprocess.run(commandline, stdout=PIPE, stderr=STDOUT,
                                universal_newlines=True, check=True, timeout=15)
    except subprocess.CalledProcessError as err:
        # Process ran but returned non-zero. If excepted, handle here.
        if err.returncode == 1 and "No supported authentication methods available" in err.stdout:
            raise ConnectionAbortedError(err.stdout) from err
        raise
    return result.stdout


def wrap_in_ssh(commandline):
    """ Takes a command line and wraps it to be executed remotely through SSH."""
    (user, host) = get_user_host()
    sshp = "/usr/bin/sshpass -f /home/cris/.ssh/ovgu-cluster-pass"
    sshc = f"/usr/bin/ssh {user}@{host} '{commandline}'"
    return shlex.split(f"{sshp} {sshc}")


def upload_to_remote():
    """ Uploading work is not a use case at this point."""
    raise NotImplementedError


def download_from_remote(target_folder):
    """ Downloads the work results from the cluster. """
    (user, host) = get_user_host()
    base_path = "/beegfs2/scratch/"
    source = f"{user}@{host}:{base_path}{user}/JOB/{target_folder}/output/"
    target = f"/home/cris/nextcloudshare/Simulations/{target_folder}/output/"
    sshp = "/usr/bin/sshpass -f /home/cris/.ssh/ovgu-cluster-pass"
    rsyn = f"rsync -av -e ssh --include '*/' --include='*.dat' --exclude='*' {source} {target}"
    commandline = shlex.split(f"{sshp} {rsyn}")

    try:
        result = subprocess.run(commandline, stdout=PIPE, stderr=STDOUT,
                                universal_newlines=True, check=True, timeout=15)
    except subprocess.CalledProcessError as err:
        # Process ran but returned non-zero. If excepted, handle here.
        print(err.returncode)
        raise
    return result.stdout


def prepare_work():
    """ Preparing the work currently happens on the remote end."""
    raise NotImplementedError


def start_numbercrunching(target_folder, mac_file):
    """ Runs the simulation on the cluster. """
    script = "/home/chifu/scratch/tmp/hemispheric_PET/run_Simulation.sh"
    command = f"{script} {target_folder} {mac_file}"
    commandline = wrap_in_ssh(command)

    try:
        result = subprocess.run(commandline, stdout=PIPE, stderr=STDOUT,
                                universal_newlines=True, check=True, timeout=15)
    except subprocess.CalledProcessError as err:
        # Process ran but returned non-zero. If excepted, handle here.
        print(err.returncode)
        raise
    return result.stdout


def finalize_work(target_folder, root_file_name):
    """ Calls the script to merge results and extract singles."""
    command = f"/home/chifu/scratch/tmp/hemispheric_PET/merge_and_extract.sh {root_file_name} {target_folder}"
    commandline = wrap_in_ssh(command)

    try:
        result = subprocess.run(commandline, stdout=PIPE, stderr=STDOUT,
                                universal_newlines=True, check=True, timeout=15)
    except subprocess.CalledProcessError as err:
        # Process ran but returned non-zero. If excepted, handle here.
        print(err.returncode)
        raise
    return result.stdout


def get_user_host():
    """ Provides login info."""
    USER = "chifu"
    HOST = "141.44.5.38"
    return (USER, HOST)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Feed me!')
    parser.add_argument('targetfolder_macfile', 
                        nargs='+', 
                        metavar='target_folder mac_file', 
                        help='one or more pairs of (target folder, mac file) seperated by a space')
    arguments = parser.parse_args()

    if len(arguments.targetfolder_macfile) % 2:
        parser.error('Found odd number of arguments. Expected pairs of target/macfile.')
    else:
        wrklist = []
        def _dualiter(singleiter):
            iterable = iter(singleiter)
            while True:
                try:
                    yield next(iterable), next(iterable)
                except StopIteration:
                    break

        for trgt_fldr, mc_file in _dualiter(arguments.targetfolder_macfile):
            wrklist.append((trgt_fldr, mc_file))

    main(wrklist)