using TimeTrackerModels;
using TimeTrackerRepository;
using TimeTrackerErrors;
using System.Globalization;
// ADD and ENUM of valid inputs
// BUG: system is not calculating time correctly
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
        if (this.isValidState("in")) {
          (string currentDate, string currentTime) = this.getDateAndTime();
          repo.addPunch(new Punch(0, "in", currentDate, currentTime, comment));

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
        if (this.isValidState("out")) {
          (string currentDate, string currentTime) = this.getDateAndTime();
          Punch lastPunch = repo.getLastPunch();  

          repo.addPunch(new Punch(0, "out", currentDate, currentTime, comment));

          Console.WriteLine(this.getTotalTime(lastPunch.time, currentTime));
          Entry entry = new Entry(0,
              currentDate,
              lastPunch.time,
              currentTime,
              this.getTotalTime(lastPunch.time, currentTime),
              lastPunch.comment + "\n" + comment);

          repo.addEntry(entry);

          return @$"
            Log: --------------------------------------------------------------
            {ErrorMessages.PunchOutSuccess}
            {ErrorMessages.EntrySucess}

            Entry: ------------------------------------------------------------
            Date: {entry.date}, {entry.timeIn} - {entry.timeOut}
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
        List<Entry> entries = repo.GetEntries(duration);

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
          }
          return output; 
        }
      }

      /// <summary>Shows punches for the given duration</summary>
      /// <param name="duration">refer to index.md for valid duration</param>
      /// <returns>
      /// list of punches in as a string
      /// if and invalid duration is given returns error message
      /// if no punches for the to returns "none"
      /// </returns>
      public string showPunches(string duration) {
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

      public void entriesToTextFile(string duration) {}

      public void punchesToTextFile(string duration) {}

      // NOTE: Unsure to seperate time and date, going to seperate
      private (string, string) getDateAndTime() {
        DateTime now = DateTime.Now;

        string currentDate = now.ToString("yyyy-MM-dd");
        string currentTime = now.ToShortTimeString();

        return (currentDate, currentTime);
      }

      private Boolean isValidState(string type) {
        Repository r = new Repository();
        Punch lastPunch  = r.getLastPunch();

        if (lastPunch == null)
          return false;
        else if (type == lastPunch.type)
          return false;
        else 
          return true;
      }

      private int getTotalTime(string inTime, string outTime) {

        DateTime t1 = DateTime.ParseExact(inTime, "h:mm tt", CultureInfo.InvariantCulture);
        DateTime t2 = DateTime.ParseExact(inTime, "h:mm tt", CultureInfo.InvariantCulture);

        TimeSpan totalTime = t2 - t1;

        return (int)totalTime.TotalHours;
      }
   }
}
