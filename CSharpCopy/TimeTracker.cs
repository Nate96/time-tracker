using TimeTrackerModels;
using TimeTrackerRepository;
using TimeTrackerErrors;
using System.Globalization;

namespace TimeTrackerApp
{
    class TimeTracker
    {
        private Repository repo;

        public TimeTracker() { this.repo = new Repository(); }

        /// <summary>Punches the user in</summary>
        /// <param name="comment">A string that will be asosiated with the punch</param>
        /// <returns> a succuess message or a error message </returns>
        public string PunchIn(string comment)
        {
            (Boolean isValidState, Punch? lastPunch) = this.IsValidState("in");

            if (isValidState)
            {
                (string currentDate, string currentTime) = this.GetDateAndTime();
                repo.AddPunch(new Punch(0, "in", currentDate, currentTime, comment));

                return ErrorMessages.PUNCHIN_SUCCESS;
            }
            return ErrorMessages.PUNCHIN_VALID;
        }

        /// <summary>Punches out user and adds entry</summary>
        /// <param name="comment">the comment that is asosicated with the punch</param>
        /// <returns>
        /// If punch out is seccesfull returns a log and the the entry that has
        /// been added.
        /// If the punch fails returns error message
        /// </returns>
        public string PunchOut(string comment)
        {
            (Boolean isValidSate, Punch? lastPunch) = this.IsValidState("out");

            if (isValidSate)
            {
                (string currentDate, string currentTime) = this.GetDateAndTime();

                repo.AddPunch(new Punch(0, "out", currentDate, currentTime, comment));

                if (lastPunch != null)
                {
                    Entry entry = new Entry(0,
                          currentDate,
                          lastPunch.time,
                          currentTime,
                          this.GetTotalTime(lastPunch.time, currentTime),
                          lastPunch.comment + "\n" + comment);

                    repo.AddEntry(entry);

                    return $"{ErrorMessages.PUNCHOUT_SUCCESS}\n{ErrorMessages.ENTRY_SUCCESS}\n{entry.ToString()}";
                }
            }
            return ErrorMessages.PUNCHOUT_INVALID;
        }

        /// <summary>Shows entries for the given duration</summary>
        ///
        /// <param name="duration">refer to index.md for valid duration</param>
        /// <returns>
        /// list of entries in as a string
        /// if and invalid duration is given returns error message
        /// if no entries for the to returns "none"
        /// </returns>
        public string ShowEntries(string duration)
        {
            List<Entry>? entries = repo.GetEntries(duration);
            float workedHours = 0;

            if (entries == null)
            {
                return ErrorMessages.INVALID_DURATION;
            }
            else if (entries.Count == 0)
            {
                return ErrorMessages.NO_ENTRIES;
            }
            else
            {
                string output = "";

                foreach (Entry entry in entries)
                {
                    output += entry.ToString() + "\n\n";
                    workedHours += entry.totalTime;
                }
                // [..^2] removes the last two chars
                return $"{output[..^2]}TOTAL: {workedHours} hours";
            }
        }

        /// <summary>Returns status of System</summary>
        /// <returns>
        /// When the last punch type was out returns most recent entry string
        /// when the last punch type was in returns most recent punch string
        /// </returns>
        public string Stats()
        {
            Punch? lastPunch = repo.GetLastPunch();
            string output = "";
            float punchInTime = 0;
            List<Entry> weekEntries = repo.GetEntries("week") ?? new List<Entry>();
            List<Entry> dayEntries = repo.GetEntries("day") ?? new List<Entry>();

            if (lastPunch == null) return "ERORR: No Punches";
            else if (lastPunch?.type == "in")
            {
               punchInTime = this.GetTotalTime(lastPunch.time, DateTime.Now.ToShortTimeString());
               output = $"Punched in for {punchInTime} hours\n{lastPunch.ToString()}\n";
            }
            else if (lastPunch?.type == "out")
            {
                List<Entry> lastEntry = repo.GetEntries("last") ?? new List<Entry>();

                if (lastEntry != null && lastEntry.Count != 0)
                    output = $"You are currently Punched out\n{lastEntry[0].ToString()}\n";
            }

            float week = weekEntries.Sum(entry => entry.totalTime);
            float day = dayEntries.Sum(entry => entry.totalTime);

            return output + $"\nDay:  {Math.Round((punchInTime + day), 2)} hours\nWeek: {Math.Round((punchInTime + week), 2)} hours";
        }

        /// <summary>
        /// Returns the current week stats in the following Format
        /// Monday:    # hours
        /// Tuesday:   # hours
        /// Wednesday: # hours
        /// Thursday:  # hours
        /// Friday:    # hours
        /// Saturday:  # hours
        /// Sunday:    # hours
        /// ------------------
        /// Total:     # hours
        /// </summary>
        /// <returns>string</returns>
        public string Report(string duration)
        { 
           const int WEEK_DAYS_NUMBER = 7;
           if (duration == "last") { duration = "last week"; }
           else { duration = "week"; }

           List<Entry> weekEntries = repo.GetEntries(duration) ?? new List<Entry>();
           float[] weekHours = new float[WEEK_DAYS_NUMBER];

           foreach (Entry entry in weekEntries)
           {
              DateTime date = DateTime.ParseExact(entry.date, "yyyy-MM-dd", CultureInfo.InvariantCulture);
              weekHours[((int)date.DayOfWeek + 6) % 7] += entry.totalTime;
           }

           return $"Monday:    {Math.Round(weekHours[0], 2)} hours\n"
                + $"Tuesday:   {Math.Round(weekHours[1], 2)} hours\n"
                + $"Wednesday: {Math.Round(weekHours[2], 2)} hours\n"
                + $"Thursday:  {Math.Round(weekHours[3], 2)} hours\n" 
                + $"Friday:    {Math.Round(weekHours[4], 2)} hours\n" 
                + $"Saturday:  {Math.Round(weekHours[5], 2)} hours\n" 
                + $"Sunday:    {Math.Round(weekHours[6], 2)} hours\n"
                + "--------------------------\n"
                + $"Todal:     {Math.Round(weekHours.Sum(), 2)} hours";
        }

        /// <summary>writes the resutls of show Entries results.md</summary>
        /// <param name="duration">refer to index.md for valid duration</param>
        /// <returns>Error or success message</returns>
        public string WriteEntries(string duration)
        {
            List<Entry>? entries = repo.GetEntries(duration);
            float totalHours = 0;

            using (StreamWriter writer = new StreamWriter("results.md"))
            {
                if (entries == null || entries.Count == 0)
                    return "WARNING: no entries";
                else
                {
                    foreach (Entry entry in entries)
                    {
                        writer.WriteLine(entry.MarkdownFormat() + "\n\n");
                        totalHours += entry.totalTime;
                    }
                    writer.WriteLine($"Total Hours Worked: {totalHours}");
                    return "SUCCESS: wrote file";
                }
            }
        }

        /// <summary>Gets the current date and the current time</summary>
        /// <returns>
        /// string: the current date in yyyy-MM-dd format
        /// string: the current time in hh:mm PM/AM format
        // NOTE: Unsure to seperate time and date, going to seperate
        private (string, string) GetDateAndTime()
        {
            DateTime now = DateTime.Now;

            string currentDate = now.ToString("yyyy-MM-dd");
            string currentTime = now.ToShortTimeString();

            return (currentDate, currentTime);
        }

        /// <summary>
        /// verifies the data is in the correct state for the action the user 
        /// wants to perform.
        /// VALID:
        /// IN - 
        /// 1. no table
        /// 2. last type = "out"
        /// OUT -
        /// 1. last type = "in"
        ///
        /// INVALID:
        /// IN - 
        /// 1. last type = "in"
        /// OUT -
        /// 1. no table
        /// 2. last type = "out"
        /// </summary>
        /// <param name="type">the action the user wants to perform</param>
        /// <returns>Boolean and a Punch Object</returns>
        private (Boolean, Punch?) IsValidState(string type)
        {
            Punch? lastPunch = repo.GetLastPunch();

            if (lastPunch == null && type == "out") return (false, null);
            else if (lastPunch == null && type == "in") return (true, null);
            else if (lastPunch?.type != type) return (true, lastPunch);
            else return (false, lastPunch);
        }

        /// <summary>calcauated the total time worked during a session</summary>
        /// <param name="inTime">string: the clock in time</param>
        /// <param name="outTime">string: the clock out time</param>
        /// <returns>float: hours worked</returns>
        private float GetTotalTime(string inTime, string outTime)
        {
            DateTime t1 = DateTime.ParseExact(inTime, "HH:mm", CultureInfo.InvariantCulture);
            DateTime t2 = DateTime.ParseExact(outTime, "HH:mm", CultureInfo.InvariantCulture);

            TimeSpan totalTime = t2 - t1;

            return (float)Math.Round(((float)totalTime.TotalMinutes / 60), 2);
        }
    }
}
