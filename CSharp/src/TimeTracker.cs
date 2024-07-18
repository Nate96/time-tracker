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

            if (lastPunch == null)
                return "No Punches";
            else if (lastPunch?.type == "in")
            {
                (string currentDate, string currentTime) = this.GetDateAndTime();
                return $"Punch in for {this.GetTotalTime(lastPunch.time, currentTime)} hours\n{lastPunch.ToString()}";
            }
            else if (lastPunch?.type == "out")
            {
                List<Entry>? lastEntry = repo.GetEntries("last");

                if (lastEntry != null && lastEntry.Count != 0)
                    return $"You are currently Punched out\n{lastEntry[0].ToString()}\n";
                else
                    return "ERROR: No Entries";
            }
            return "Default";
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

            if (lastPunch == null && type == "out")
                return (false, null);
            else if (lastPunch == null && type == "in")
                return (true, null);
            else if (lastPunch?.type != type)
                return (true, lastPunch);
            else
                return (false, lastPunch);
        }

        /// <summary>calcauated the total time worked during a session</summary>
        /// <param name="inTime">string: the clock in time</param>
        /// <param name="outTime">string: the clock out time</param>
        /// <returns>float: hours worked</returns>
        private float GetTotalTime(string inTime, string outTime)
        {
            DateTime t1 = DateTime.ParseExact(inTime, "h:mm tt", CultureInfo.InvariantCulture);
            DateTime t2 = DateTime.ParseExact(outTime, "h:mm tt", CultureInfo.InvariantCulture);

            TimeSpan totalTime = t2 - t1;

            return (float)Math.Round(((float)totalTime.TotalMinutes / 60), 2);
        }
    }
}
