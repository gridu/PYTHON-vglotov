import subprocess
import logging
import sys

from shlex import split

logging.basicConfig(
    format='[%(asctime)s : %(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%I:%M:%S')
LOGGER = logging.getLogger()


def execute_cmd_on_host(_user, _host, _script):
    LOGGER.info("Running script on behalf of " + _user + " user on host " + _host)
    cmd = split("ssh {}@{} \'{}\'".format(_user, _host, _script))
    cmd_output = str(subprocess.check_output(cmd))[2:-3].split('\\n')
    if cmd_output != ['']:
        LOGGER.info(cmd_output)


if __name__ == '__main__':

    host = 'localhost'
    user = 'vglotov'
    script = 'echo TEST_ME > test.txt'

    if len(sys.argv) == 4:
        host = sys.argv[1]
        user = sys.argv[2]
        script = sys.argv[3]
    elif len(sys.argv) == 1:
        pass
    else:
        LOGGER.warning("Execution terminated")
        sys.exit("Incorrect number of arguments passed: there should be 3 or none")

    execute_cmd_on_host(user, host, script)
    execute_cmd_on_host(user, host, 'ls')
