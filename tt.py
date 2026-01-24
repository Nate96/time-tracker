#!/user/bin/env Python3

import argparse
import presenter
import punch_clock

from config import Res, MESSAGES
from time_sheet import Punch

if __name__ == '__main__':
    args = None
    punch_clock = punch_clock

    parser = argparse.ArgumentParser(
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                        prog='tt',
                        description='punch in punch out system',
                        epilog='''
Actions:
  p "your comment" Punches in/out
  status           Shows the state of the time sheet (in or out)
  report           Shows the total worked hours for each day, and the total for
                   the current week
  show last        Shows the last entry
  show day         Shows all entries for the day
  show week        Shows all entries for the week
  show month       Shows all entries for the month
                                ''')

    parser.add_argument('action', help='refer to actions')
    parser.add_argument('comment', nargs='?', default='', help='strings that are tied to the punch')

    # Parse all command line arguments
    args = parser.parse_args(args)

    if args.action in ("p", "punch"):
        results = punch_clock.punch(args.comment)

        if isinstance(results, Punch):
            presenter.show_punch(results)
        else:
            presenter.show_entry(results)

    elif args.action == "show": presenter.show_entries(args.comment)
    elif args.action == "status": presenter.show_state()
    elif args.action == "report": presenter.report(args.comment)
    else: print(MESSAGES[Res.INVALID_COMMAND])
