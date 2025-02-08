using TimeTrackerModels;
using TimeTrackerRepository;
using TimeTrackerErrors;
using TimeTrackerPresenter;


namespace TimeTrackerApp
{
    class TimeTracker
    {
        private Repository repo;

        public TimeTracker() { this.repo = new Repository(); }

        /// <summary>
        ///    Punches the user in
        /// </summary>
        /// <param name="comment"> comment for the Entry </param>
        /// <returns>
        ///    a success message or a error message
        /// </returns>
        public string PunchIn(string comment)
        {
            (Boolean isValidState, Punch? lastPunch) = this.IsValidState("in");

            if (isValidState && repo.AddPunch("in", comment))
                return ErrorMessages.PUNCHIN_SUCCESS
                     + "\n" + repo.GetLastPunch().ToString();
            return ErrorMessages.PUNCHIN_VALID;
        }

        /// <summary>
        ///    Punches out user and adds entry
        /// </summary>
        /// <param name="comment"> title for the Entry
        /// <returns>
        ///    If punch out is successful returns a log and the entry that
        ///    has been added. If the punch fails returns error message
        /// </returns>
        public string PunchOut(string comment)
        {
            (Boolean isValidSate, Punch? lastPunch) = this.IsValidState("out");

            if (isValidSate)
            {
                repo.AddPunch("out", comment);

                if (repo.AddEntry())
                {
                   List<Entry>? lastEntry = repo.GetEntries("last");
                   return Presenter.PunchOutSuccess(lastEntry[0].ToString());
                }
            }
            return ErrorMessages.PUNCHOUT_INVALID;
        }

        /// <summary>
        ///    Shows entries for the given duration
        /// </summary>
        /// <param name="duration"></param>
        /// <returns>
        ///    list of entries in as a string if and invalid duration is given
        ///    returns error message if no entries for the to returns "none"
        /// </returns>
        public string ShowEntries(string duration)
        {
            List<Entry>? entries = repo.GetEntries(duration);
            float workedHours = 0;

            if (entries == null)
                return ErrorMessages.INVALID_DURATION;
            else if (entries.Count == 0)
                return ErrorMessages.NO_ENTRIES;
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

        /// <summary>
        ///    Returns status of System</summary>
        /// <returns>
        ///    When the last punch type was out returns most recent entry string
        ///    when the last punch type was in returns most recent punch string
        /// </returns>
        /// NOTE: Duplicate Data with day and week lists
        public string Status()
        {
            Punch lastPunch = repo.GetLastPunch();
            List<Entry> dayEntries = repo.GetEntries("day");
            List<Entry> weekEntries = repo.GetEntries("week");

            switch (lastPunch.type)
            {
               case "in":
                  return Presenter.InStatus(lastPunch, dayEntries, weekEntries);
               case "out":
                  List<Entry> lastEntry = repo.GetEntries("last");
                  return Presenter.outStatus(lastEntry[0], dayEntries, weekEntries);
               default:
                  return ErrorMessages.NO_ENTRIES;
            }
        }

        /// <summary>
        ///    writes the results of show Entries results.md
        /// </summary>
        /// <param name="duration">refer to index.md for valid duration</param>
        /// <returns>
        ///    Error or success message
        /// </returns>
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

        ///<summary>
        ///    Calculates hours worked through out the week, and outputs the 
        ///    results of is outputed via [Req7] formate
        /// </summary>
        public string Report() 
        {
           List<Entry> weekEntries = repo.GetEntries("week") ?? new List<Entry>();
           return Presenter.reportWeekHours(weekEntries);
        }

        /// <summary>
        ///    verifies the data is in the correct state for the action the user 
        ///    wants to perform.
        ///    VALID:
        ///    IN - 
        ///    1. no table
        ///    2. last type = "out"
        ///    OUT -
        ///    1. last type = "in"
        ///
        ///    INVALID:
        ///    IN - 
        ///    1. last type = "in"
        ///    OUT -
        ///    1. no table
        ///    2. last type = "out"
        /// </summary>
        /// <param name="type">the action the user wants to perform</param>
        /// <returns>
        ///    Boolean and a Punch Object
        /// </returns>
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
    }
}
