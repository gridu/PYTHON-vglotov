import subprocess
import logging
import sys

logging.basicConfig(
    format='[%(asctime)s : %(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%I:%M:%S')
LOGGER = logging.getLogger()

if __name__ == '__main__':

    host = 'localhost'
    user = 'vglotov'

    if len(sys.argv) == 3:
        host = sys.argv[1]
        user = sys.argv[2]
    if len(sys.argv) == 2 or len(sys.argv) > 3:
        LOGGER.warning("Execution terminated")
        sys.exit("Incorrect number of arguments passed: there should be 2 or none")

    LOGGER.info("Running script on behalf of " + user + " user on host " + host)
    cmd = "ssh {}@{} 'echo TEST_ME > test.txt'".format(user, host)

    subprocess.run(cmd, shell=True)
    subprocess.run('ls', shell=True)

