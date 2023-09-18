from datetime import datetime, timedelta, time
import click


def _display_results(hours):
    print(f'Total hours worked today: {round(hours, 2)}')
    print(f'%50: {round(hours / 2, 2)} \n%25: {round(hours/4, 2)}')


def _normal_mode(intime, outtime):
    """Normal Mode
    Calculates total time (hours) by using a start time and an end time.
    Then, displays the results.
    """
    start_strip = datetime.strptime(intime, "%H:%M")
    end_strip = datetime.strptime(outtime, "%H:%M")

    delta = end_strip - start_strip

    sec = delta.total_seconds()
    hours = sec / (60 * 60)
    _display_results(hours)


def _friday_mode(intime, totaltime):
    """Friday Mode
    Calculates time to leave and hours need to be worked on Friday.
    Then, Displays the results
    """
    remaining_hours = 40.0 - totaltime

    delta_time = datetime.strptime(intime, "%H:%M") + timedelta(hours=remaining_hours)

    delta_hour = delta_time.time().hour % 12

    print(f'You get to work until: {time(delta_hour, delta_time.time().minute)}')
    _display_results(remaining_hours)


@click.command()
@click.option('-mode', '-m',
              type=str,
              default='n',
              required=False,
              help='Mode: n = normal, f = friday')
@click.option('-intime', '-i',
              type=str,
              required=False,
              help='In Time: HH:MM')
@click.option('-outtime', '-o',
              type=str,
              required=False,
              help='In Time: HH:MM')
@click.option('-totaltime', '-tl',
              type=float,
              help='In Time: HH:MM')
@click.option('-comment', '-c',
              type=str,
              required=False,
              help='Comment for entry')
def time_tracker(mode, intime, outtime, totaltime, comment):
    if mode == 'n':
        _normal_mode(intime, outtime)
    elif mode == 'f':
        _friday_mode(intime, totaltime)


if __name__ == '__main__':
    time_tracker()
    # TODO: Add SQLight DB for messages
