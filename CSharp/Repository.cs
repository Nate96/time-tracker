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

       if (this.isValidState("in")) {
          var command = connection.CreateCommand();

          (string currentDate, string currentTime) = this.GetDateAndTime();

          command.CommandText = @"
             INSERT INTO punch (type, punch_date, punch_time, comment)
             VALUES($type, $currentDate, $currentTime, $comment)";

          command.Parameters.AddWithValue("type", "in");
          command.Parameters.AddWithValue("$currentDate", currentDate);
          command.Parameters.AddWithValue("$currentTime", currentTime);
          command.Parameters.AddWithValue("$comment", comment);

          if (command.ExecuteNonQuery() == 1) {
             connection.Close();
             return "Punched in successfully";
          } else {
             connection.Close();
             return "A Error has accurded, punch was not added";
          }
       }

       connection.Close();
       return "ERROR message for db state not valid, cannot punch in";


       //last punch in an out
       // get current day
       // get current time

       // open connection to database
       // add [currentdate, time, type, comment] 
    }

    public String PunchOut(string comment) {
       SqliteConnection connection = this.ConnectToDatabase();

       if (this.isValidState("out")) {
          var command = connection.CreateCommand();

          (string currentDate, string currentTime) = this.GetDateAndTime();

          command.CommandText = @"
             INSERT INTO punch (type, punch_date, punch_time, comment)
             VALUES($type, $currentDate, $currentTime, $comment)";

          command.Parameters.AddWithValue("$type", "out");
          command.Parameters.AddWithValue("$currentDate", currentDate);
          command.Parameters.AddWithValue("$currentTime", currentTime);
          command.Parameters.AddWithValue("$comment", comment);

          if (command.ExecuteNonQuery() == 1) {
             connection.Close();
          } else {
             connection.Close();
             return "A Error has accurded, punch was not added";
          }

          connection = this.ConnectToDatabase();
          command = connection.CreateCommand();

          command.CommandText = @"
             INSERT INTO punch (type, punch_date, punch_time, comment)
             VALUES($type, $currentDate, $currentTime, $comment)";

          
       }
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

    // NOTE: Unsure to seperate time and date, going to seperate
    private (string, string) GetDateAndTime() {
       DateTime now = DateTime.Now;

       string currentDate = now.ToString("yyyy-MM-dd-DDD");
       string currentTime = now.ToShortTimeString();

       return (currentDate, currentDate);
    }

    private Boolean isValidState(string type) {
       SqliteConnection connection = this.ConnectToDatabase();
       var command = connection.CreateCommand();

 //       command.CommandText = 
 //          @"SELECT * 
 //          FROM punch
 //          ORDER BY Id DESC
 //          LIMIT 1";
 //
 //       var reader = command.ExecuteReader();
 //
 //       // table is empty
 //       if (type == "out" && !reader.Read()) {
 //          connection.Close();
 //
 //          return false;
 //       }
 //
       return true;
    }

  }
}
