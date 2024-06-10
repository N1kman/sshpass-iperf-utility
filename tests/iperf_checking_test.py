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
        mock_args.return_value = Mock(host=self.HOST, user=self.USER, password=self.PASSWORD, file=False)
        args = get_args()
        self.assertEqual(args.host, self.HOST)
        self.assertEqual(args.user, self.USER)
        self.assertFalse(args.file)
        self.assertEqual(args.password, self.PASSWORD)

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
