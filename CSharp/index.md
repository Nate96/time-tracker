# SET UP 
1. install dotnet
    Windows: winget install Microsoft.DotNet.SDK.8
    Ubuntu:  sudo snap install dotnet-sdk --classic
    MAC:     brew install --cask dotnet
2. Install SQLite3: dotnet add package Microsoft.Data.Sqlite

# How to use
dotnot run i *punch in*
dotnot run o "Comment" *punch in*

[Main](Program.cs)

# Notes
Create Project: dotnet new console -n microsoft.time-tracker -f net6.0
