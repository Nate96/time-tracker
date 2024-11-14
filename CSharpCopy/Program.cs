// TODO: Fix null ref warnings

using TimeTrackerApp;

class Program
{
      static void Main(string[] args) {
         string comment = "";
         string mode = args[0];
         if (args.Length == 2) { comment = args[1]; }

         TimeTracker timeTracker = new TimeTracker();

         switch (mode) {
            case "i":
               Console.WriteLine(timeTracker.PunchIn(comment));
               break;
            case "o":
               Console.WriteLine(timeTracker.PunchOut(comment));
               break;
            case "show":
               Console.WriteLine(timeTracker.ShowEntries(comment));
               break;
            case "write":
               Console.WriteLine(timeTracker.WriteEntries(comment));
               break;
            case "status":
               Console.WriteLine(timeTracker.Stats());
               break;
            case "report":
               Console.WriteLine(timeTracker.Report(comment));
               break;

            default:
               Console.WriteLine(TimeTrackerErrors.ErrorMessages.INVALID_INPUT);
               break;
         }
         return;
      }
}
