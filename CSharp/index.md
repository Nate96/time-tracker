# SET UP 
1. install dotnet
    Windows: winget install Microsoft.DotNet.SDK.8
    Ubuntu:  sudo snap install dotnet-sdk --classic
    MAC:     brew install --cask dotnet-sdk 
2. Install SQLite3: dotnet add package Microsoft.Data.Sqlite

# How to use
dotnot run i "Comment" *punch in*
dotnot run o "Comment" *punch in*
dotnot run show "day" *shows entries today*
dotnot run show "week" *shows entries for the current week*
dotnot run show "month" *shows entries for the current month*
dotnot run show "quart" *shows entries for the current quarter*
dotnot run show "year" *shows entries for the current current*

[Main](Program.cs)

# TODOs 
- Logging

# Notes
Create Project: dotnet new console -n microsoft.time-tracker -f net6.0
