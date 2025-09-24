# Time Tracker
A simple CLI tool that tracks time while completing tasks. 

# Commands

|     Command      |                     Description                                      |
|:-----------------|:---------------------------------------------------------------------|   
| i "your comment" | punch in                                                             |
| o "your comment" | punch out, creates a new entry, and prints the  entry to the console |
| show last        | prints last entry to the console                                     |
| show day         | prints entries to the console for the current day                    |
| show week        | prints entries to the console for the current week                   |
| show month       | prints entries to the console for the current month                  |
| status           | show whether the user is punched in or out                           |
| report           | show the hours worked each day of the current week                   |

# Installation  
1. Install Python3
2. run `git pull https://www.github.com/Nate96/time-tracker.git`
3. In the time-tracker directory run `make verify` to verify the app is working 
   correctly
4. In the time-tracker directory run `make install`
