import unittest
from unittest import TestCase
from unittest.mock import patch, Mock

from sshpass_utils import SshExecuter

class SshpassTest(TestCase):

    HOST = '192.168.0.1'
    NO_CONNECTION = 'No connection to'
    MANY_TIMES = 'So many cheking times'

    @patch('subprocess.Popen')
    def test_execute_command(self, mock_popen):
        sshExecuter = SshExecuter(user='user', host=self.HOST)
        mock_popen.return_value = Mock(**{'communicate.return_value': (b'output', b'error'), 'returncode': 1})

        output, error, code = sshExecuter.execute_command('command')

        self.assertEqual('output', output)
        self.assertEqual('error', error)
        self.assertEqual(1, code)


if __name__ == "__main__":
    unittest.main()