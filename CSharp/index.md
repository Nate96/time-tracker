# set up 
1. install dotnet
    windows: winget install microsoft.dotnet.sdk.8
    ubuntu:  sudo snap install dotnet-sdk --classic
    mac:     brew install --cask dotnet-sdk 
2. install sqlite3: dotnet add package microsoft.data.sqlite

# how to use
dotnet run i "comment"      *punch in*
dotnet run o "comment"      *punch in and print entry to the console*
dotnet run show "day"       *prints entires to the console for the current day*
dotnet run show "week"      *prints entires to the console for the current week*
dotnet run show "month"     *prints entires to the console for the current month*
dotnet run write "day"      *writes entires to the result.md file for the current day*
dotnet run write "week"     *writes entires to the result.md file for the current week*
dotnet run write "month"    *writes entires to the result.md file for the current month*

[main](program.cs)

# todos 
- logging
- writing to file

# notes
create project: dotnet new console -n microsoft.time-tracker -f net6.0
