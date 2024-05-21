using Microsoft.Data.Sqlite;
using TimeTrackerModels;

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

        private SqliteConnection ConnectToDatabase()
        {
            SqliteConnection connection = new SqliteConnection(DatabaseLocation);
            connection.Open();

            return connection;
        }


        public Punch getLastPunch()
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


        public Boolean addPunch(Punch punch)
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

        public Boolean addEntry(Entry entry)
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

        public Entry[] getEntries(string duration) { return []; }
    }
}
