from iperf_utils import IperfExecuter
import json
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--host', type=str, required=True)
    parser.add_argument('-u', '--user', type=str, required=True)
    parser.add_argument('-f', '--file', action='store_true', help='password from file')
    parser.add_argument('-p', '--password', type=str, required=False)
    return parser.parse_args()


def main() -> None:
    try:
        args = get_args()
        iperf = IperfExecuter(user=args.user, host=args.host, password=args.password, pass_from_file=args.file)
        res = iperf.execute_analyze(args.host)
        print(json.dumps({"error": "None", "result": json.loads(res), "status": 0}, indent=4))
    except Exception as e:
        print(json.dumps({"error": str(e), "result": "None", "status": -1}, indent=4))


if __name__ == '__main__':
    main()
