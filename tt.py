from datetime import datetime, timedelta, time
import click


def _display_results(hours):
    print(f'Total hours worked today: {round(hours, 2)}')
    print(f'%50: {round(hours / 2, 2)} \n%25: {round(hours/4, 2)}')


def _normal_mode(in_time, out_time):
    """Normal Mode
    Calculates total time (hours) by using a start time and an end time.
    Then, displays the results.
    """
    start_strip = datetime.strptime(in_time, "%H:%M")
    end_strip = datetime.strptime(out_time, "%H:%M")

    delta = end_strip - start_strip

    sec = delta.total_seconds()
    hours = sec / (60 * 60)
    _display_results(hours)


def _friday_mode(in_time, total_time):
    """Friday Mode
    Calculates time to leave and hours need to be worked on Friday.
    Then, Displays the results
    """
    remaining_hours = 40.0 - total_time

    delta_time = datetime.strptime(in_time, "%H:%M") + timedelta(hours=remaining_hours)

    delta_hour = delta_time.time().hour % 12

    print(f'You get to work until: {time(delta_hour, delta_time.time().minute)}')
    _display_results(remaining_hours)


@click.command()
@click.option('-m', '--mode',
              type=str,
              default='n',
              required=True,
              help='Mode: n = normal, f = friday')
@click.option('-i', '--in-time',
              type=str,
              required=False,
              help='In Time: HH:MM')
@click.option('-o', '--out-time',
              type=str,
              required=False,
              help='In Time: HH:MM')
@click.option('-tl', '--total_time',
              type=float,
              help='In Time: HH:MM')
@click.option('-c', '--comment',
              type=str,
              required=False,
              help='Comment for entry')
def time_tracker(mode, in_time, out_time, total_time, comment):
    if mode == 'n':
        _normal_mode(in_time, out_time)
    elif mode == 'f':
        _friday_mode(in_time, total_time)


if __name__ == '__main__':
    print("tt")
    time_tracker()
    # TODO: Add SQLight DB for messages
