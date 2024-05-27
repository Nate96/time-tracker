using Microsoft.Data.Sqlite;
using TimeTrackerModels;

//NOTE: DateTime.Now is in localtime

namespace TimeTrackerRepository
{
    class Repository
    {
        private const string DatabaseLocation = ("Data Source=../Log.db");

        public Repository()
        {
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
            totalTime FLOAT NOT NULL,
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

        /// <summary>connects to the given database</summary>
        /// <returns>SqliteConnection</return>
        private SqliteConnection ConnectToDatabase()
        {
            SqliteConnection connection = new SqliteConnection(DatabaseLocation);
            connection.Open();

            return connection;
        }


        /// <summary>Returns the most recent row in the Punch Table</summary>
        /// <returns>Punch</returns>
        public Punch? GetLastPunch()
        {
            SqliteConnection connection = this.ConnectToDatabase();
            var command = connection.CreateCommand();

            command.CommandText =
              @"SELECT *
              FROM punch
              ORDER BY Id DESC
              LIMIT 1";

            var reader = command.ExecuteReader();

            // table is empty
            if (!reader.Read()) {
                connection.Close();
                return null;
            }
            else {
                int id = reader.GetInt32(0);
                string type = reader.GetString(1);
                string punchDate = reader.GetString(2);
                string punchTime = reader.GetString(3);
                string comment = reader.GetString(4);

                connection.Close();
                return new Punch(id, type, punchDate, punchTime, comment);
            }
        }

        /// <summary>adds to the punch table</summary>
        /// <param name="punch">Punch</param>
        /// <returns>
        /// true when the row is added successfully and false when the row is
        /// not added successfully
        /// </returns>
        public Boolean AddPunch(Punch punch)
        {
            SqliteConnection connection = this.ConnectToDatabase();
            var command = connection.CreateCommand();

            command.CommandText = @"
              INSERT INTO punch (type, punch_date, punch_time, comment)
              VALUES($type, $currentDate, $currentTime, $comment)";

            command.Parameters.AddWithValue("type", punch.type);
            command.Parameters.AddWithValue("$currentDate", punch.date);
            command.Parameters.AddWithValue("$currentTime", punch.time);
            command.Parameters.AddWithValue("$comment", punch.comment);

            if (command.ExecuteNonQuery() == 1)
            {
                connection.Close();
                return true;
            }
            else
            {
                connection.Close();
                return false;
            }
        }

        /// <summary>Adds a row to the entry table</summary>
        /// <param name="entry">Entry</param>
        /// <returns>
        /// true when the row is added successfully and false when the row is
        /// not added successfully
        /// </returns>
        public Boolean AddEntry(Entry entry)
        {
            SqliteConnection connection = this.ConnectToDatabase();
            connection = this.ConnectToDatabase();
            var command = connection.CreateCommand();

            command.CommandText = @"
              INSERT INTO  entry (entry_date, timeIn, timeOut, totalTime, comment)
              VALUES($date, $timeIn, $timeOut, $totalTime, $comment)";

            command.Parameters.AddWithValue("$date", entry.date);
            command.Parameters.AddWithValue("$timeIn", entry.timeIn);
            command.Parameters.AddWithValue("$timeOut", entry.timeOut);
            command.Parameters.AddWithValue("$totalTime", entry.totalTime);
            command.Parameters.AddWithValue("$comment", entry.comment);

            if (command.ExecuteNonQuery() == 1)
            {
                connection.Close();
                return true;
            }
            else
            {
                connection.Close();
                return false;
            }
        }

        /// <summary>Get entries with the given duration</summary>
        /// <param name="duration">the time span of the entries</param>
        /// <returns>A list of Entries object<returns>
        public List<Entry>? GetEntries(string duration) {
          SqliteConnection connection = this.ConnectToDatabase();
          var command = connection.CreateCommand();

          switch(duration) {
            case "day":
              command.CommandText = @"
                SELECT *
                FROM entry
                WHERE entry_date == (SELECT date('now', 'localtime'))";
              break;
            case "week":
              command.CommandText = @"
                 SELECT * 
                 FROM entry
                 WHERE entry_date > (SELECT date('now', 'localtime', $move))";
              Console.WriteLine((int)DateTime.Now.DayOfWeek);
              command.Parameters.AddWithValue("$move", $"{-(int)DateTime.Now.DayOfWeek} days");
              break;
            case "month":
              command.CommandText = @"
                 SELECT * 
                 FROM entry
                 WHERE entry_date > (SELECT date('now', 'localtime', $move))";
              Console.WriteLine((int)DateTime.Now.Day-1);
              command.Parameters.AddWithValue("$move", $"{-(int)DateTime.Now.Day} days");
              break;
            case "last":
              command.CommandText = @"
                 SELECT *
                 FROM entry
                 ORDER BY Id DESC
                 LIMIT 1";
              break;
            default:
              return null;
          }

          List<Entry> entries = new List<Entry>();
          var reader = command.ExecuteReader();
          while (reader.Read()) {
            entries.Add(new Entry(reader.GetInt32(0),
                  reader.GetString(1),
                  reader.GetString(2),
                  reader.GetString(3),
                  reader.GetFloat(4),
                  reader.GetString(5)));
          }

          connection.Close();
          return entries;
        }
    }
}
