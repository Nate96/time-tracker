import click
from time_tracker import normal_mode, friday_mode, execute_query, get_todays_entries, get_hours_worked


@click.command()
@click.option('-m', '--mode',
              type=str,
              default='n',
              required=True,
              help='Mode: n = normal, f = friday, q = querying mode, d = today entry(s)')
@click.option('-i', '--in-time',
              type=str,
              required=False,
              help='In Time: HH:MM')
@click.option('-o', '--out-time',
              type=str,
              required=False,
              help='In Time: HH:MM')
@click.option('-hw', '--hours-worked',
              type=float,
              help='In Time: HH:MM')
@click.option('-c', '--comment',
              type=str,
              required=False,
              help='Comment for entry')
@click.option('-q', '--query',
              type=str,
              required=False,
              help='SQLite query')
def time_tracker(mode, in_time, out_time, hours_worked, comment, query):
    if mode == 'n':
        normal_mode(in_time, out_time)
    elif mode == 'f':
        friday_mode(in_time, hours_worked)
    elif mode == 'q':
        execute_query(query)
    elif mode == 'd':
        get_todays_entries()
    elif mode == 'tt':
        get_hours_worked_today()


if __name__ == '__main__':
    time_tracker()
