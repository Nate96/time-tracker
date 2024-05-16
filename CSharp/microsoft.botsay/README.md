# SET UP 
1. install dotnet
    Windows: winget install Microsoft.DotNet.SDK.8
    Linux:   sudo apt-get install -y dotnet-sdk-8.0
    MAC:     brew install --cask dotnet
2. Create: Project dotnet new console -n microsoft.botsay -f net6.0
3. Install SQLite3: dotnet add package Microsoft.Data.Sqlite
