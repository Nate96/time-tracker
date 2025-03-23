#!/user/bin/env python3

import argparse
import punch_clock
import json
import presenter

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

    if args.one == "i" or args.one == "in":
        print(punch_clock.punch_in(args.two))
    elif args.one == "o" or args.one == "out":
        print(punch_clock.punch_out(args.two))
    elif args.one == "show":
        print(presenter.show_entrie(args.two))
    elif args.one == "status":
        print(presenter.status())
    elif args.one == "report":
        print(presenter.report(args.two))
    else:
        print(MESSAGES["InvalidCommand"])
