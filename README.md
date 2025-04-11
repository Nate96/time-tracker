# Time Tracker
A simple CLI tool that tracks time while completing tasks. 

# Commands

|     Command      |                     Description                       |
|:-----------------|:------------------------------------------------------|
| i "your comment" | punch in                                              |
| o "your comment" | punch in and print entry to the console               |
| show last        | prints last entry to the console                      |
| show day         | prints entries to the console for the current day     |
| show week        | prints entries to the console for the current week    |
| show month       | prints entries to the console for the current month   |
| status           | show whether the user is punched in or out            |
| report           | show the hours worked each day of the current week    |

# Installation  

## C#
1. install dotnet  
2. run `git checkout C#`
2. Add the abosulte paths for files in CSharp/scr/models/config.cs  
3. run `dotnet build --configuration Release`  
4. Add to command line  
    - zsh: add "export PATH=$PATH:{path to repo}/bin/Release/netX.0" to .zshrc
    - windows PowerShell: Set-Alias -Name tt -Value "{path to exe}"

## Python
1. install Python3
2. run `git checkout Python`
3. Add .env file
   ```
   REPO_PATH=''
   TARGET_WORK_HOURS=5;
   MAX_WORK_WEEK_DAYS=5;
   TRACK=false;
   ```
4. Add to command line
    - add alias to zsh: alias tt ="Python3 {path to tt.py}"
    - windows PowerShell: Set-Alias -Name tt -Value "Python3 {path to tt.py}"
