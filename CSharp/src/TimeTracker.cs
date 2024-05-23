using TimeTrackerModels;
using TimeTrackerRepository;
using TimeTrackerErrors;
using System.Globalization;

// ADD and ENUM of valid inputs

namespace TimeTrackerApp {
   class TimeTracker {
     private Repository repo;

      public TimeTracker() {
        this.repo = new Repository();
      }

      /// <summary>Punches the user in</summary>
      /// <param name="comment">A string that will be asosiated with the punch</param>
      /// <returns> a succuess message or a error message </returns>
      public string PunchIn(string comment) {
        (Boolean isValidState, Punch? lastPunch) = this.IsValidState("out");

        if (isValidState) {
          (string currentDate, string currentTime) = this.GetDateAndTime();
          repo.AddPunch(new Punch(0, "in", currentDate, currentTime, comment));

          return ErrorMessages.PunchInSuccess;
        }
        return ErrorMessages.PunchInInvalid;
      }

      /// <summary>Punches out user and adds entry</summary>
      /// <param name="comment">the comment that is asosicated with the punch</param>
      /// <returns>
      /// If punch out is seccesfull returns a log and the the entry that has
      /// been added.
      /// If the punch fails returns error message
      /// </returns>
      public string PunchOut(string comment) {
        (Boolean isValidSate, Punch? lastPunch) = this.IsValidState("out");

        if (isValidSate && lastPunch != null) {
          (string currentDate, string currentTime) = this.GetDateAndTime();
          
          repo.AddPunch(new Punch(0, "out", currentDate, currentTime, comment));

          Entry entry = new Entry(0,
              currentDate,
              lastPunch.time,
              currentTime,
              this.GetTotalTime(lastPunch.time, currentTime),
              lastPunch.comment + "\n" + comment);

          repo.AddEntry(entry);

          return @$"
            Log: --------------------------------------------------------------
            {ErrorMessages.PunchOutSuccess}
            {ErrorMessages.EntrySucess}

            Entry: ------------------------------------------------------------
            Date: {entry.date}, {entry.timeIn} - {entry.timeOut}
            Time Worked: {entry.totalTime}
            {entry.comment}"; 
        }
        return ErrorMessages.PunchOutInvalid;
      }

      /// <summary>Shows entries for the given duration</summary>
      /// <param name="duration">refer to index.md for valid duration</param>
      /// <returns>
      /// list of entries in as a string
      /// if and invalid duration is given returns error message
      /// if no entries for the to returns "none"
      /// </returns>
      public string ShowEntries(string duration) {
        List<Entry>? entries = repo.GetEntries(duration);
        float workedHours = 0;

        if (entries == null) {
          return ErrorMessages.INVALID_DURATION;
        } else if (entries.Count == 0) {
          return ErrorMessages.NO_ENTRIES;
        } else {
          string output = "";

          foreach (Entry entry in entries) {
            output += $"Date: {entry.date}\n";
            output += $"Punch time: In-{entry.timeIn} Out-{entry.timeOut}\n";
            output += $"Total Time: {entry.totalTime}\n";
            output += $"Comment: \n{entry.comment}\n";
            output += "\n";

            workedHours += entry.totalTime;
          }
          return output + "\n" + "Hours Worked today:" + workedHours; 
        }
      }

      /// <summary>Shows punches for the given duration</summary>
      /// <param name="duration">refer to index.md for valid duration</param>
      /// <returns>
      /// list of punches in as a string
      /// if and invalid duration is given returns error message
      /// if no punches for the to returns "none"
      /// </returns>
      public string ShowPunches(string duration) {
        List<Punch> punches = repo.GetPunches(duration);
        string output = "";

        foreach (Punch punch in punches) {
          output += $"Type: {punch.type}\n";
          output += $"Date: {punch.date}\n";
          output += $"Time: {punch.time}\n";
          output += $"Comment: \n{punch.comment}\n";
          output += "\n";
        }
        return output;
      }

      /// <summary>writes the resutls of show Entries to a markdown file</summary>
      /// <param name="duration">refer to index.md for valid duration</param>
      // TODO:
      public void EntriesToTextFile(string duration) {}

      /// <summary>writes the resutls of show Entries to a markdown file</summary>
      /// <param name="duration">refer to index.md for valid duration</param>
      // TODO:
      public void PunchesToTextFile(string duration) {}

      /// <summary>Gets the current date and the current time</summary>
      /// <returns>
      /// string: the current date in yyyy-MM-dd format
      /// string: the current time in hh:mm PM/AM format
      // NOTE: Unsure to seperate time and date, going to seperate
      private (string, string) GetDateAndTime() {
        DateTime now = DateTime.Now;

        string currentDate = now.ToString("yyyy-MM-dd");
        string currentTime = now.ToShortTimeString();

        return (currentDate, currentTime);
      }

      /// <summary>
      /// verifies the data is in the correct state for the action the user 
      /// wants to perform.
      /// </summary>
      /// <param name="type">the action the user wants to perform</param>
      /// <returns>Boolean and a Punch Object</returns>
      private (Boolean, Punch?) IsValidState(string type) {
        Punch? lastPunch = repo.GetLastPunch();

        if (lastPunch == null && type == "out")
          return (false, lastPunch);
        else if (type == lastPunch?.type)
          return (false, lastPunch);
        else 
          return (true, lastPunch);
      }

      /// <summary>calcauated the total time worked during a session</summary>
      /// <param name="inTime">string: the clock in time</param>
      /// <param name="outTime">string: the clock out time</param>
      /// <returns>float: hours worked</returns>
      private float GetTotalTime(string inTime, string outTime) {
        DateTime t1 = DateTime.ParseExact(inTime, "h:mm tt", CultureInfo.InvariantCulture);
        DateTime t2 = DateTime.ParseExact(outTime, "h:mm tt", CultureInfo.InvariantCulture);

        TimeSpan totalTime = t2 - t1;
        Console.WriteLine($"in: {inTime}");
        Console.WriteLine($"out: {outTime}");
        Console.WriteLine($"Total Time: {(float)totalTime.TotalMinutes / 60}");

        return (float)Math.Round(((float)totalTime.TotalMinutes / 60), 2);
      }
   }
}
