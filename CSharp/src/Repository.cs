using Microsoft.Data.Sqlite;
using System.Globalization;

namespace Repository{
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
            comment TEXT NOT NULL)";

      command.ExecuteNonQuery();
      connection.Close();
    }

    public String PunchIn(string comment) {
       SqliteConnection connection = this.ConnectToDatabase();

       if (this.isValidState("in")) {
          Console.WriteLine(this.isValidState("in"));
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
       Console.WriteLine("ERROR message for db state not valid, cannot punch in");
       return "ERROR message for db state not valid, cannot punch in";
    }

    public String PunchOut(string comment) {
       SqliteConnection connection = this.ConnectToDatabase();

       Console.WriteLine(this.isValidState("out"));
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

          // Add entry 
          connection = this.ConnectToDatabase();
          command = connection.CreateCommand();

          command.CommandText = @"
             INSERT INTO  entry (entry_date, timeIn, timeOut, totalTime, comment)
             VALUES($date, $timeIn, $timeOut, $totalTime, $comment)";

          (string type, string inDate, string inTime, string inComment) = this.getLastPunch();

          command.Parameters.AddWithValue("$date", currentDate);
          command.Parameters.AddWithValue("$timeIn", inTime);
          command.Parameters.AddWithValue("$timeOut", currentTime);
          command.Parameters.AddWithValue("$totalTime", this.getTotalTime(inTime, currentTime));
          command.Parameters.AddWithValue("$comment", inComment + "/n" + comment);

          if (command.ExecuteNonQuery() == 1) {
            connection.Close();
            return "Punched in successfully";
          } else {
            connection.Close();
            return "A Error has accurded, punch was not added";
          }
       }
       else {
          Console.WriteLine("Data base is in an invalid state to punch out");
          return "Data base is in an invalid state to punch out";
       }
    }

    private SqliteConnection ConnectToDatabase() {
       SqliteConnection connection = new SqliteConnection(DatabaseLocation);
       connection.Open();

       return connection;
    }

    // NOTE: Unsure to seperate time and date, going to seperate
    private (string, string) GetDateAndTime() {
       DateTime now = DateTime.Now;

       string currentDate = now.ToString("yyyy-MM-dd");
       string currentTime = now.ToShortTimeString();

       return (currentDate, currentTime);
    }

    // TODO: implement
    private Boolean isValidState(string type) {
      (string lastType, string punchDate, string punchTime, string comment) = getLastPunch();
      Console.WriteLine("lastType: " + lastType + " current type: " + type);

      if (type == "out" && lastType == "" && punchDate == "" && punchTime == "" && comment == "")
         return false;
      else if (type == lastType)
         return false;
      else 
       return true;
    }

    private (string, string, string, string) getLastPunch() {
      SqliteConnection connection = this.ConnectToDatabase();
      var command = connection.CreateCommand();

      command.CommandText = 
        @"SELECT type, punch_date, punch_time, comment
        FROM punch
        ORDER BY Id DESC
        LIMIT 1";

      var reader = command.ExecuteReader();

      // table is empty
      if (!reader.Read()) {
        connection.Close();
        return ("", "", "", "");

      } else {
        string type = reader.GetString(0);
        string punchDate = reader.GetString(1);
        string punchTime = reader.GetString(2);
        string comment = reader.GetString(3);

        connection.Close();
        return (type, punchDate, punchTime, comment);
      }
    }

    private int getTotalTime(string inTime, string outTime) {

      DateTime t1 = DateTime.ParseExact(inTime, "h:mm tt", CultureInfo.InvariantCulture);
      DateTime t2 = DateTime.ParseExact(inTime, "h:mm tt", CultureInfo.InvariantCulture);


//      TimeSpan t1 = TimeSpan.Parse(inTime);
//      TimeSpan t2 = TimeSpan.Parse(outTime);

      TimeSpan totalTime = t2 - t1;

      return (int)totalTime.TotalHours;
    }
  }
}
