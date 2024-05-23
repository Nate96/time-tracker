// TODO: Fix null ref warnings
using TimeTrackerApp;

class Program
{
      static void Main(string[] args)
      {
         if (args.Length != 2) {
           Console.WriteLine(TimeTrackerErrors.ErrorMessages.INVALID_INPUT);
           return;
         }

         string mode = args[0];
         string comment = args[1];

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
            default:
               Console.WriteLine(TimeTrackerErrors.ErrorMessages.INVALID_INPUT);
               break;
         }
         return;
      }
}
