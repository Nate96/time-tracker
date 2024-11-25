#!/user/bin/env python3

import argparse
import time_tracker
import json

if __name__ == '__main__':
    args = None
    MESSAGES = json.load(open("../Dialogue/CommandErrors.json"))

    parser = argparse.ArgumentParser(
                        prog='Time Tracker',
                        description='punch in punch out system',
                        epilog='Hello')

    parser.add_argument('one')
    parser.add_argument('two', nargs='?', default='')

    # Parse all command line arguments
    args = parser.parse_args(args)

    if args.one == "i":
        print(time_tracker.punch_in(args.two))
    elif args.one == "o":
        print(time_tracker.punch_out(args.two))
    elif args.one == "show":
        print(time_tracker.show_entrie(args.two))
    elif args.one == "status":
        print(time_tracker.status())
    elif args.one == "report":
        print(time_tracker.report(args.two))
    else:
        print(MESSAGES["InvalidCommand"])
