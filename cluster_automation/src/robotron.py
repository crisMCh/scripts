#https://peps.python.org/pep-0008/

import time
import os
import subprocess
from subprocess import PIPE, STDOUT

def main():
    ''' Meow '''
    print("Henlo, worlf!")

    #upload_to_remote()
    #prepare_work()
    #start_numbercrunching()
    wait_for_numbercrunching()
    #finalize_work()
    #download_from_remote()


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

    # TODO: implement Q status parsing
    # Make sure to test that at least some expected string was returned (e.g. table header)
    print(queue_status)
    if "cris" in queue_status:
        empty = False
    elif "HEADER" in queue_status:
        empty = True
    else:
        raise ValueError("Unexpected queue status response")
    return empty


def get_queue_status():
    ''' Runs a command to get the current queue status. '''
    command = ["ls", "-la"]     # TODO: replace with command to get Q status
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
    user = "cris"
    host = "criegsulikk.lan.jonthe.net"

    user_host = f"{user}@{host}"
    # unpack original list of args into a single string
    remote_cmd = f"{' '.join(commandline)}"

    if os.name == "posix":
        wrapped = ["ssh", user_host, remote_cmd]
    elif os.name == "nt":
        where_is_the_klink = r"C:\ProgramData\chocolatey\bin\klink.exe"
        wrapped = [where_is_the_klink, '-batch', user_host, remote_cmd]
    else:
        raise NotImplementedError
    return wrapped


def upload_to_remote():
    raise NotImplementedError

def download_from_remote():
    raise NotImplementedError

def prepare_work():
    ''' Could run the splitter. '''
    raise NotImplementedError

def start_numbercrunching():
    ''' Could feed the beast. '''
    raise NotImplementedError

def finalize_work():
    ''' Could run the merger. '''
    raise NotImplementedError


if __name__ == "__main__":
    main()
