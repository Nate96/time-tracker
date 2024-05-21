using TimeTrackerModels;
using TimeTrackerRepository;
using TimeTrackerErrors;
using System.Globalization;

namespace TimeTrackerApp {
   class TimeTracker {
     private Repository repo;

      public TimeTracker() {
        this.repo = new Repository();
      }

      public string PunchIn(string comment) {
        if (this.isValidState("in")) {
          (string currentDate, string currentTime) = this.getDateAndTime();
          repo.addPunch(new Punch(0, "in", currentDate, currentTime, comment));

          return ErrorMessages.PunchInSuccess;
        }
        return ErrorMessages.PunchInInvalid;
      }

      public string PunchOut(string comment) {
        if (this.isValidState("out")) {
          (string currentDate, string currentTime) = this.getDateAndTime();
          Punch lastPunch = repo.getLastPunch();  

          repo.addPunch(new Punch(0, "out", currentDate, currentTime, comment));
          Entry entry = new Entry(0, currentDate, lastPunch.time, currentTime, this.getTotalTime(lastPunch.time, currentTime), lastPunch.comment + "\n" + comment);
          repo.addEntry(entry);

          return @$"
            Log: --------------------------------------------------------------
            {ErrorMessages.PunchOutSuccess}
            {ErrorMessages.EntrySucess}

            Entry: ------------------------------------------------------------
            Date: {entry.date}, {entry.timeIn} - {entry.timeOut}
            {comment}"; 
        }
        return ErrorMessages.PunchOutInvalid;
      }

      public string showEntries(string duration) {return ""; }

      public string showPunches(string duration) {return ""; }

      public void toEntriesFile(string duration) {}

      public void toPunchesFile(string duration) {}

      // NOTE: Unsure to seperate time and date, going to seperate
      private (string, string) getDateAndTime() {
        DateTime now = DateTime.Now;

        string currentDate = now.ToString("yyyy-MM-dd");
        string currentTime = now.ToShortTimeString();

        return (currentDate, currentTime);
      }

      // TODO: implement
      private Boolean isValidState(string type) {
        Repository r = new Repository();
        Punch lastPunch  = r.getLastPunch();

        Console.WriteLine($"last: {lastPunch.type}, current type: {type}");

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
