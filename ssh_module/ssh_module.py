import subprocess
import logging
import argparse

from getpass import getuser
from shlex import split

logging.basicConfig(
    format='[%(asctime)s : %(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%I:%M:%S')
LOGGER = logging.getLogger()


def execute_cmd_on_host(_user, _host, _script):
    LOGGER.info('Running script on behalf of %s user on host %s', _user, _host)
    cmd = 'ssh {}@{} \'{}\''.format(_user, _host, _script)
    # Method subprocess.check_output() returns byte sequence starting with "b'" symbols and ending with "\n'".
    # Hence [2:-3] is used to avoid useless in our case symbols before and after command output.
    # For example 'ls' command will return next byte sequence: b'Folder_name\nfile_name.txt\n'
    cmd_output = str(subprocess.check_output(split(cmd), timeout=20))[2:-3].split('\\n')
    LOGGER.info('Command executing: %s', cmd)
    LOGGER.info('Command output: %s', cmd_output)


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--host', type=str, default='localhost')
    PARSER.add_argument('--user', type=str, default=getuser())
    PARSER.add_argument('--script', type=str, default='echo TEST_ME > ~/Desktop/test.txt')
    ARGS = PARSER.parse_args()

    host = ARGS.host
    user = ARGS.user
    script = ARGS.script

    execute_cmd_on_host(user, host, script)
    execute_cmd_on_host(user, host, 'cd Desktop && ls')
