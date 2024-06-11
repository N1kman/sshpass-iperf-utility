import unittest
from unittest import TestCase
from unittest.mock import patch, Mock

from sshpass_utils import SshExecuter
from iperf_utils import IperfExecuter

class IperfCheckingTest(TestCase):

    HOST = '192.168.0.1'
    NO_CONNECTION = 'No connection to'
    MANY_TIMES = 'So many cheking times'

    @patch('threading.Thread')
    @patch('sshpass_utils.SshExecuter.execute_command')
    def test_execute_analyze_with_except(self, mock_ssh_executer, mock_thread):
        iperfExecuter = IperfExecuter(user1='user', host1=self.HOST, user2='user', host2=self.HOST)

        mock_ssh_executer.return_value = ('output', 'error', 1)

        thread_mock = Mock()
        mock_thread.return_value = thread_mock

        SshExecuter.stop_process = Mock()
        SshExecuter.stop_process.return_value = None

        SshExecuter.is_running = Mock()
        SshExecuter.is_running.return_value = False

        self.check_res_with_exception(iperfExecuter, self.MANY_TIMES)
        thread_mock.start.assert_called_once()

        SshExecuter.is_running.return_value = True
        self.check_res_with_exception(iperfExecuter, self.NO_CONNECTION)

    @patch('threading.Thread')
    @patch('sshpass_utils.SshExecuter.execute_command')
    def test_execute_analyze(self, mock_ssh_executer, mock_thread):
        iperfExecuter = IperfExecuter(user1='user', host1=self.HOST, user2='user', host2=self.HOST)

        mock_ssh_executer.return_value = ('output', 'error', 0)

        thread_mock = Mock()
        mock_thread.return_value = thread_mock

        SshExecuter.is_running = Mock()
        SshExecuter.is_running.side_effect = [True, False]

        self.assertEqual('output', iperfExecuter.execute_analyze())


    def check_res_with_exception(self, iperfExecuter, message):
        with self.assertRaises(Exception) as context:
            iperfExecuter.execute_analyze()
        self.assertTrue(message in str(context.exception))


if __name__ == "__main__":
    unittest.main()
