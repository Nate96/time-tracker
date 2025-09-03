#!/user/bin/env Python3

import argparse
import time_tracker
from config import Res, MESSAGES

if __name__ == '__main__':
    args = None
    punch_clock = time_tracker

    parser = argparse.ArgumentParser(
                        prog='Time Tracker',
                        description='punch in punch out system',
                        epilog='Hello')

    parser.add_argument('one')
    parser.add_argument('two', nargs='?', default='')

    # Parse all command line arguments
    args = parser.parse_args(args)

    if args.one == "i":
        res: Res = punch_clock.punch_in(args.two)
        print(MESSAGES[res])
    elif args.one == "o":
        res: Res = punch_clock.punch_out(args.two)
        print(MESSAGES[res])
    elif args.one == "show":
        print(punch_clock.show_entrie(args.two))
    elif args.one == "status":
        print(punch_clock.status())
    elif args.one == "report":
        print(punch_clock.report(args.two))
    else:
        print(MESSAGES["INVALID_COMMNAD"])
