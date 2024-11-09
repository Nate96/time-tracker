# set up 
1. install dotnet
    windows: winget install microsoft.dotnet.sdk.8
    ubuntu:  sudo snap install dotnet-sdk --classic
    mac:     brew install --cask dotnet-sdk 
2. dotnet run build

# notes
create project: dotnet new console -n microsoft.time-tracker -f net6.0
install sqlite3: dotnet add package microsoft.data.sqlite

