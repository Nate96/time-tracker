import argparse
import time_tracker
import json
import logging


if __name__ == '__main__':
    args = None
    MESSAGES = json.load(open("../Messages/CommandErrors.json"))
    logging.basicConfig(filename='tt.log', level=logging.INFO)

    parser = argparse.ArgumentParser(
                        prog='ProgramName',
                        description='What the program does',
                        epilog='Text at the bottom of help')

    parser.add_argument('one')
    parser.add_argument('two', nargs='?', default='')

    # Parse all command line arguments
    args = parser.parse_args(args)

    if args.one == "i":
        time_tracker.punch_in(args.two)
    elif args.one == "o":
        time_tracker.punch_out(args.two)
    elif args.one == "show":
        time_tracker.show_entrie(args.two)
    elif args.one == "status":
        time_tracker.status()
    elif args.one == "report":
        time_tracker.report(args.two)
    else:
        print(MESSAGES["InvalidCommand"])

    print(args.two)
    print(args.one) 
