from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk
import tkinter as tk

def display_results(hours):
    """
    Displays hour distributed by charge codes
    """
    return f'Total Hours: {round(hours,2)} \n50%: {round(hours/2, 2)} \n25%: {round(hours/4, 2)}'


def nomral_mode():
    """Normal Mode
    Calculates total time (hours) by using a start time and an end time. 
    Then, displays the results.
    """
    start_strip = datetime.strptime(start_time.get(), "%H:%M")
    end_strip = datetime.strptime(end_time.get(), "%H:%M")

    delta = end_strip - start_strip

    sec = delta.total_seconds()
    hours = sec / (60 * 60)

    Message(frm, text=display_results(hours)).grid(column=0, row=4, pady=5)



def friday_mode():
    """Friday Mode
    Calculates time to leave and hours need to be worked on Friday. 
    Then, Displays the results
    """
    total_time = float(total_hours_worked.get())
    remaining_hours = 40.0 - total_time

    time_out = datetime.strptime(start_time.get(), "%H:%M") + timedelta(hours=remaining_hours)

    Message(frm, text=f"End time {time_out.time()}\n" + display_results(remaining_hours)).grid(column=0, row=4, pady=5)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Time Tracker")
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    
    start_time = tk.StringVar()
    end_time = tk.StringVar()
    total_hours_worked = tk.StringVar()

    ttk.Label(frm, text="Start Time:").grid(column=0, row= 0, pady=5)
    ttk.Entry(frm, textvariable=start_time).grid(column=1, row=0, pady=5)
    ttk.Label(frm, text="End Time:").grid(column=0, row= 1, pady=5)
    ttk.Entry(frm, textvariable=end_time).grid(column=1, row=1, pady=5)
    ttk.Label(frm, text="Total Hours:").grid(column=0, row= 2, pady=5)
    ttk.Entry(frm, textvariable=total_hours_worked).grid(column=1, row=2, pady=5)
    ttk.Button(frm, text="Normal", command=nomral_mode).grid(column=0, row=3, pady=5)
    ttk.Button(frm, text="Friday Mode", command=friday_mode).grid(column=1, row=3,pady=5)
    Message(frm, text="Out put").grid(column=0, row=4, pady=5)
    root.mainloop()