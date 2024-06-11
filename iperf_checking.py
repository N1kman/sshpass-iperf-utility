from iperf_utils import IperfExecuter
import json
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host1', type=str, required=True)
    parser.add_argument('--user1', type=str, required=True)
    parser.add_argument('--file1', action='store_true', help='password from file')
    parser.add_argument('--password1', type=str, required=False)
    parser.add_argument('--host2', type=str, required=True)
    parser.add_argument('--user2', type=str, required=True)
    parser.add_argument('--file2', action='store_true', help='password from file')
    parser.add_argument('--password2', type=str, required=False)
    return parser.parse_args()


def main() -> None:
    try:
        args = get_args()
        iperf = IperfExecuter(user1=args.user1, host1=args.host1, password1=args.password1, pass_from_file1=args.file1,
                              user2=args.user2, host2=args.host2, password2=args.password2, pass_from_file2=args.file2)
        res = iperf.execute_analyze()
        print(json.dumps({"error": "None", "result": json.loads(res), "status": 0}, indent=4))
    except Exception as e:
        print(json.dumps({"error": str(e), "result": "None", "status": -1}, indent=4))


if __name__ == '__main__':
    main()
