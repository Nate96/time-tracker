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
            type TEXT NOT NULL,
            punch_date DATE NOT NULL,
            punch_time TIME NOT NULL,
            comment TEXT NOT NULL,)";

      command.ExecuteNonQuery();
      connection.Close();
    }

    public String PunchIn(string comment) {
       SqliteConnection connection = this.ConnectToDatabase();
       var command = connection.CreateCommand();

       command.CommandText = @"
          INSERT INTO punch (type, punch_date, punch_time, comment)
          VALUES($type, $currentDate, $currentTime, $comment)";

       command.Parameters.AddWithValue("type", "in");
       command.Parameters.AddWithValue("$currentDate", currentDate);
       command.Parameters.AddWithValue("$currentTime", currentTime);
       command.Parameters.AddWithValue("$comment", comment);

       connection.Close();

       if (command.ExecuteNonQuery() == 1) {
          Console.WriteLine("Punched in successfully");
       } else {
          Console.WriteLine("A Error has accurded, punch was not added");
       }

       command.CommandText = 
          @"SELECT * 
            FROM punch
            ORDER BY Id DESC
            LIMIT 1";

       var reader = command.ExecuteReader();

       // table is empty
       if (!reader.Read()) {
          connection.Close();
          connection = this.ConnectToDatabase();
          command = connection.CreateCommand();

          Console.WriteLine("Have not punched in yet");
       }

       //last punch in an out
       // get current day
       // get current time

       // open connection to database
       // add [currentdate, time, type, comment] 
       return "";
    }

    public String PunchOut(string comment) {
       //open a connetion
       //check if table is empty or check if most recent punch is "in"

       // get current day
       // get current time

       // open connection to database
       // add [currentdate, time, type, comment]
       // close db connection
       return "";
    }

    private SqliteConnection ConnectToDatabase() {
       SqliteConnection connection = new SqliteConnection(DatabaseLocation);
       connection.Open();

       return connection;
    }

    // RESEARCH can return multiple values in c#
    private object GetDataAndTime() {
       return null;
    }

  }
}
