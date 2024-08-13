using Microsoft.Data.Sqlite;
using TimeTrackerModels;

//NOTE: DateTime.Now is in localtime

namespace TimeTrackerRepository
{
    class Repository
    {
        private const string DATABASE_LOCATION = "Data Source=../Test/Log.db";
        private const string CREATE_TABLE      = "../SqlScripts/CreateTables.sql";
        private const string LAST_PUNCH        = "../SqlScripts/GetLastPunch.sql";
        private const string INSERT_PUNCH      = "../SqlScripts/InsertPunch.sql";
        private const string INSERT_ENTRY      = "../SqlScripts/InsertEntry.sql";
        private const string TODAY             = "../SqlScripts/GetTodayEntry.sql";
        private const string WEEK              = "../SqlScripts/GetWeekEntry.sql";
        private const string MONTH             = "../SqlScripts/GetMonthEntry.sql";
        private const string LAST_ENTRY        = "../SqlScripts/GetLastEntry.sql";

        public Repository()
        {
            SqliteConnection connection = new SqliteConnection(DATABASE_LOCATION);

            var command = connection.CreateCommand();

            connection.Open();
            connection.CreateCommand();
            command.CommandText = File.ReadAllText(CREATE_TABLE);
            command.ExecuteNonQuery();
            connection.Close();
        }

        /// <summary>connects to the given database</summary>
        /// <returns>SqliteConnection</return>
        private SqliteConnection ConnectToDatabase()
        {
            SqliteConnection connection = new SqliteConnection(DATABASE_LOCATION);
            connection.Open();

            return connection;
        }

        /// <summary>Returns the most recent row in the Punch Table</summary>
        /// <returns>Punch</returns>
        public Punch? GetLastPunch()
        {
            SqliteConnection connection = this.ConnectToDatabase();
            var command = connection.CreateCommand();

            command.CommandText = File.ReadAllText(LAST_PUNCH);

            var reader = command.ExecuteReader();

            // table is empty
            if (!reader.Read())
            {
                connection.Close();
                return null;
            }
            else
            {
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

            command.CommandText = File.ReadAllText(INSERT_PUNCH);
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

            command.CommandText = File.ReadAllText(INSERT_ENTRY);
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
        public List<Entry>? GetEntries(string duration)
        {
            SqliteConnection connection = this.ConnectToDatabase();
            var command = connection.CreateCommand();

            switch (duration)
            {
                case "day":
                    command.CommandText = File.ReadAllText(TODAY);
                    break;
                case "week":
                    command.CommandText = File.ReadAllText(WEEK);
                    command.Parameters.AddWithValue("$move", $"{-(int)DateTime.Now.DayOfWeek} days");
                    break;
                case "month":
                    command.CommandText = File.ReadAllText(MONTH);
                    command.Parameters.AddWithValue("$move", $"{-(int)DateTime.Now.Day} days");
                    break;
                case "last":
                    command.CommandText = File.ReadAllText(LAST_ENTRY);
                    break;
                default:
                    return null;
            }

            List<Entry> entries = new List<Entry>();
            var reader = command.ExecuteReader();
            while (reader.Read())
            {
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
