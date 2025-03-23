#!/user/bin/env python3

import argparse
import punch_clock
import json
import presenter as PRS
import repository as REPO

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
        res = punch_clock.punch_in()

        if res == -1:
            print(MESSAGES['PUNCHIN_SUCCESS'])
        elif res == 0:
            print(MESSAGES['PUNCHIN_SUCCESS'])
        if res == 1:
            print(MESSAGES['PUNCHIN_SUCCESS'])
            print(REPO.show_entrie("last"))
            print(PRS.format_punch(REPO.get_last_punch()))

        print(punch_clock.punch_in(args.two))
    elif args.one == "o" or args.one == "out":
        print(punch_clock.punch_out(args.two))
        res = punch_clock.punch_in()

        if res == -1:
            print(MESSAGES['PUNCHIN_SUCCESS'])
        elif res == 0:
            print(MESSAGES['PUNCHIN_SUCCESS'])
        if res == 1:
            print(MESSAGES['PUNCHIN_SUCCESS'])
            print(REPO.show_entrie("last"))
            print(PRS.format_punch(REPO.get_last_punch()))
    elif args.one == "show":
        print(PRS.show_entrie(args.two))
    elif args.one == "status":
        print(PRS.status())
    elif args.one == "report":
        print(PRS.report(args.two))
    else:
        print(MESSAGES["InvalidCommand"])
