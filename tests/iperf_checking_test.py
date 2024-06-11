import json
import unittest
from unittest import TestCase
from unittest.mock import patch, Mock

from iperf_checking import get_args
from iperf_checking import main


class IperfUtilityTest(TestCase):
    HOST = '192.168.0.3'
    USER = 'user'
    PASSWORD = 'pass'
    TEST_JSON = "test result"

    @patch('argparse.ArgumentParser.parse_args')
    def test_get_args(self, mock_args):
        mock_args.return_value = Mock(host1=self.HOST, user1=self.USER, password1=self.PASSWORD, file1=False,
                                      host2=self.HOST, user2=self.USER, password2=self.PASSWORD, file2=False)
        args = get_args()
        self.assertEqual(args.host1, self.HOST)
        self.assertEqual(args.user1, self.USER)
        self.assertFalse(args.file1)
        self.assertEqual(args.password1, self.PASSWORD)
        self.assertEqual(args.host2, self.HOST)
        self.assertEqual(args.user2, self.USER)
        self.assertFalse(args.file2)
        self.assertEqual(args.password2, self.PASSWORD)

    @patch('iperf_checking.get_args')
    @patch('iperf_utils.IperfExecuter.execute_analyze')
    def test_main(self, mock_execute_analyze, mock_get_args):
        mock_get_args.return_value = Mock(host=self.HOST, user=self.USER, password=self.PASSWORD, file=False)
        mock_execute_analyze.return_value = json.dumps(self.TEST_JSON)
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_once_with(
                json.dumps({"error": "None", "result": "test result", "status": 0}, indent=4))


if __name__ == "__main__":
    unittest.main()
