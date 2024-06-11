from sshpass_utils import SshExecuter
import threading
import subprocess
import time


class IperfExecuter:

    COMMAND_IPERF = 'iperf3 -s -1'

    CHECKING_TIME_SEC = 1
    CHECKING_TIMES = 10

    def __init__(self, *, user1, host1, user2, host2, password1=None, pass_from_file1=False, password2=None, pass_from_file2=False):
        self.ssh_executer_1 = SshExecuter(user=user1, host=host1, password=password1, pass_from_file=pass_from_file1)
        self.ssh_executer_2 = SshExecuter(user=user2, host=host2, password=password2, pass_from_file=pass_from_file2)
        self.server_ip = host1

    def execute_analyze(self):
        process_thread = threading.Thread(target=self.ssh_executer_1.execute_command, args=(self.COMMAND_IPERF,))
        process_thread.start()

        self.__checking_is_running(False)

        stdout, error, return_code = self.ssh_executer_2.execute_command(f'iperf3 -c {self.server_ip} -J')

        if return_code:
            self.ssh_executer_1.stop_process(self.COMMAND_IPERF)
            raise Exception(f'No connection to {self.server_ip}.')

        self.__checking_is_running()

        return stdout

    def __checking_is_running(self, running=True):
        times = 0
        while self.ssh_executer_1.is_running() == running:
            time.sleep(self.CHECKING_TIME_SEC)
            times += 1
            if times > self.CHECKING_TIMES:
                raise Exception('So many cheking times')
