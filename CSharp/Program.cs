// TODO: Seperate functionality of the Repository Class to another class
//  Link: https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design
// TODO: Create Object with all error messages
//
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
            default:
               Console.WriteLine(TimeTrackerErrors.ErrorMessages.INVALID_INPUT);
               break;
         }
         return;
      }
}
