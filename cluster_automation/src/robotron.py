#https://peps.python.org/pep-0008/

import time
import os
import subprocess
from subprocess import PIPE, STDOUT
import argparse

def main(worklist):
    ''' Automation script for running and retrieving work on the Uni computing cluster.
        The script needs to run on a machine with ssh access to the cluster (through VPN).
        Accepts a list with an arbitrary number of pairs (target_folder, macfile) to be 
        processed sequentially.
    '''
    print("Robotron awakes!")

    for (target_folder, mac_file) in worklist:
        print((target_folder, mac_file))
        print("\n")
        #upload_to_remote()
        #prepare_work()
        start_numbercrunching(target_folder, mac_file)
        wait_for_numbercrunching()
        finalize_work(target_folder, mac_file)
        wait_for_numbercrunching()
        download_from_remote(target_folder)


def wait_for_numbercrunching(timeout=(24 * 60 * 60)):
    ''' Sleeps until the queue has finished. Raises TimeoutError 
    if timeout in seconds has expired before.'''
    poll_interval = 1       # in seconds # TODO: slow down adequately
    while not my_queue_isempty():
        timeout -= poll_interval
        if timeout > 0:
            print("Still waiting")
            time.sleep(poll_interval)
        else:
            raise TimeoutError("Timed out waiting for queue to finish")


def my_queue_isempty():
    ''' Parses the queue status to check if the queue is finished. '''
    queue_status = get_queue_status()
    empty = False
    
    (USER, _) = get_user_host()
    if USER in queue_status:
        empty = False
    # Test that at least some expected string was returned (e.g. table header)
    elif "JOBID" in queue_status:
        empty = True
    else:
        print(queue_status)
        raise ValueError("Unexpected queue status response")
    return empty


def get_queue_status():
    ''' Runs a command to get the current queue status. '''

    command = ["squeue", "-u $USER"]
    commandline = wrap_in_ssh(command)

    try:
        result = subprocess.run(commandline, stdout=PIPE, stderr=STDOUT, 
                                text=True, check=True, timeout=15)
    except subprocess.CalledProcessError as err:
        # Process ran but returned non-zero. If excepted, handle here.
        if err.returncode == 1 and "No supported authentication methods available" in err.stdout:
            raise ConnectionAbortedError(err.stdout) from err
        print(err.returncode)
        raise
    return result.stdout


def wrap_in_ssh(commandline):
    ''' Takes a command line and wraps it to be executed remotely through SSH. '''

    LIVE = False
    (USER, HOST) = get_user_host()
    user_host = f"{USER}@{HOST}"
    # unpack original list of args into a single string
    remote_cmd = f"{' '.join(commandline)}"

    if LIVE:
        wrapped = ["sshpass -f .ssh/ovgu-cluster-pass ssh", user_host, remote_cmd]
    else:
        user_host = "cris@criegsulikk.lan.jonthe.net"
        remote_cmd = "ls -la"
        where_is_the_klink = r"C:\ProgramData\chocolatey\bin\klink.exe"
        wrapped = [where_is_the_klink, '-batch', user_host, remote_cmd]
    return wrapped


def upload_to_remote():
    ''' Uploading work is not a use case at this point.'''
    raise NotImplementedError

def download_from_remote(target_folder):
    ''' Downloads the work results from the cluster. '''
    (USER, HOST) = get_user_host()
    BASE_PATH = "/beegfs2/scratch/"
    source = f"{USER}@{HOST}:{BASE_PATH}{USER}/JOB/{target_folder}/output/"
    target = f"~cris/nextcloudshare/Simulations/{target_folder}/output/"

    commandline = ["sshpass -f .ssh/ovgu-cluster-pass rsync", "-av", "-e ssh", "--include '*/'", "--include='*.dat'", "--exclude='*'", source, target]

    try:
        result = subprocess.run(commandline, stdout=PIPE, stderr=STDOUT, 
                                text=True, check=True, timeout=15)
    except subprocess.CalledProcessError as err:
        # Process ran but returned non-zero. If excepted, handle here.
        print(err.returncode)
        raise
    
    return result.stdout



def prepare_work():
    ''' Preparing the work currently happens on the remote end.'''
    raise NotImplementedError


def start_numbercrunching(target_folder, mac_file):
    ''' Runs the simulation on the cluster. '''
    
    # ./run_Simulation.sh <Name-of-target-folder> <main-mac-file-to-call>
    command = ["./run_Simulation.sh", target_folder, mac_file]
    commandline = wrap_in_ssh(command)

    try:
        result = subprocess.run(commandline, stdout=PIPE, stderr=STDOUT, 
                                text=True, check=True, timeout=15)
    except subprocess.CalledProcessError as err:
        # Process ran but returned non-zero. If excepted, handle here.
        print(err.returncode)
        raise
    return result.stdout


def finalize_work(target_folder, root_file_name):
    ''' Calls the script to merge results and extract singles. '''

    # Usage: ./merge_and_extract.sh root-file-name output-folder
    command = ["./merge_and_extract.sh", root_file_name, target_folder]
    commandline = wrap_in_ssh(command)

    try:
        result = subprocess.run(commandline, stdout=PIPE, stderr=STDOUT, 
                                text=True, check=True, timeout=15)
    except subprocess.CalledProcessError as err:
        # Process ran but returned non-zero. If excepted, handle here.
        print(err.returncode)
        raise
    return result.stdout

def get_user_host():
    USER = "chifu"
    HOST = "141.44.5.38"
    return (USER, HOST)

if __name__ == "__main__":
    def dualiter(singleiter):
        iterable = iter(singleiter)
        while True:
            try:
                yield next(iterable), next(iterable)
            except StopIteration:
                break

    parser = argparse.ArgumentParser(description='Feed me!')
    parser.add_argument('targetfolder_macfile', nargs='+')
    args = parser.parse_args()
    
    if len(args.targetfolder_macfile) % 2:
        parser.error('filepairs arg should be pairs of values')
    else:
        worklist = []
        for targetfolder, macfile in dualiter(args.targetfolder_macfile):
            worklist.append((targetfolder, macfile))

    main(worklist)