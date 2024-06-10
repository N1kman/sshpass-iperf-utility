import subprocess
from typing import Tuple


class SshExecuter:
    PASSWORD_FILE_PATH = "./sshpass_utils/password"

    def __init__(self, *, host, user, password=None, pass_from_file=False, protocol_scp=False):
        self.__password, self.__option = self.__check_pass(password, pass_from_file)
        self.__protocol = self.__check_protocol(protocol_scp)
        self.__host = host
        self.__user = user
        self.__process = None

    def execute_command(self, command: str) -> Tuple[str, str, int]:
        """
        :return:
            stdout
            stderr
            returncode
        """
        params = f'sshpass {self.__option} {self.__password} {self.__protocol} {self.__user}@{self.__host} {command}'
        self.__process = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = self.__process.communicate()
        return stdout.decode('UTF-8'), stderr.decode('UTF-8'), self.__process.returncode

    def is_running(self) -> bool:
        if self.__process is not None:
            if self.__process.poll() is None:
                return True
        return False

    @staticmethod
    def __check_pass(password: str, pass_from_file: bool) -> Tuple[str, str]:
        if password is None:
            password = SshExecuter.PASSWORD_FILE_PATH
            pass_from_file = True
        if pass_from_file is True:
            return password, '-f'
        return password, '-p'

    @staticmethod
    def __check_protocol(protocol_scp: bool) -> str:
        if protocol_scp is True:
            return 'scp'
        return 'ssh'
