#!/user/bin/env Python3

import argparse
import presenter
import punch_clock

from config import Res, MESSAGES
from punch_clock import State

if __name__ == '__main__':
    args = None
    punch_clock = punch_clock

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
        print(presenter.show_last_punch())

    elif args.one == "o":
        res: Res = punch_clock.punch_out(args.two)
        print(MESSAGES[res])
        print(presenter.show_last_entry())

    elif args.one == "show":
        presenter.show_entries(args.two)

    elif args.one == "status":
        rsl: State = punch_clock.status()
        print(MESSAGES[rsl.res])
        day_total: float = 0.0

        if rsl.res != Res.NO_PUNCH:
            if  rsl.res == Res.IN:
                day_total: float = rsl.get_punched_in_for()

                print(presenter.show_punch(rsl.last_punch), '\n')
                print(f'For:  {day_total:.2f} hours')
            else:
                print(presenter.show_entry(rsl.last_entry), '\n')
            print(f'Day:  {day_total + rsl.get_day_total():.2f} hours')
            print(f'Week: {day_total + rsl.get_week_total():.2f} hours')

    elif args.one == "report":
        print(presenter.report())
    else:
        print(MESSAGES[Res.INVALID_COMMAND])
