from sshpass_utils import SshExecuter
import threading
import subprocess
import time


class IperfExecuter:

    COMMAND_IPERF = 'iperf3 -s -1'

    CHECKING_TIME_SEC = 1
    CHECKING_TIMES = 10

    def __init__(self, *, user, host, password=None, pass_from_file=False):
        self.sshExecuter = SshExecuter(user=user, host=host, password=password, pass_from_file=pass_from_file)

    def execute_analyze(self, server_ip):
        process_thread = threading.Thread(target=self.sshExecuter.execute_command, args=(self.COMMAND_IPERF,))
        process_thread.start()

        self.__checking_is_running(False)

        process = subprocess.Popen(f'iperf3 -c {server_ip} -J', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()

        if process.returncode:
            raise Exception(f'No connection to {server_ip}')

        self.__checking_is_running()

        return stdout.decode('utf-8')

    def __checking_is_running(self, running=True):
        times = 0
        while self.sshExecuter.is_running() == running:
            time.sleep(self.CHECKING_TIME_SEC)
            times += 1
            if times > self.CHECKING_TIMES:
                raise Exception('So many cheking times')
