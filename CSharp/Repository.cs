using Microsoft.Data.Sqlite;

namespace RepositoryNameSpace {
  class Repository {
    private const string DatabaseLocation = ("Data Source=../Log.db");

    public Repository() {
      SqliteConnection connection = new SqliteConnection(DatabaseLocation);

      var command = connection.CreateCommand();

      //Create Entry Table
      connection.Open();
      connection.CreateCommand();

      command.CommandText = 
        @"CREATE TABLE IF NOT EXISTS entry(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            entry_date DATE NOT NULL,
            timeIn TIME NOT NULL,
            timeOut TIME NOT NULL,
            totalTime INTEGER NOT NULL,
            comment TEXT NOT NULL)";

      command.ExecuteNonQuery();
      connection.Close();

      //Create Punch Table
      connection.Open();
      connection.CreateCommand();

      command.CommandText = 
        @"CREATE TABLE IF NOT EXISTS  punch(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            date DATE NOT NULL,
            punch_time TIME NOT NULL,
            type TEXT NOT NULL)";

      command.ExecuteNonQuery();
      connection.Close();
    }
  }
}
