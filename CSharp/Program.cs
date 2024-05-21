// TODO: Seperate functionality of the Repository Class to another class
//  Link: https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design
// TODO: Create Object with all error messages
//
using RepositoryNameSpace;

class Program
{
   const string INVALID_INPUT = "In-vaild input. Refer to index.md in the 'How to Use' section";

      static void Main(string[] args)
      {
         if (args.Length != 2) {
            Console.WriteLine(INVALID_INPUT);
            return;
         }

         string mode = args[0];
         string comment = args[1];

         Console.WriteLine(mode);
         Console.WriteLine(comment);

         Repository repository = new Repository();

         switch (mode) {
            case "i":
               repository.PunchIn(comment);
               break;
            case "o":
               repository.PunchOut(comment);
               break;
            default:
               Console.WriteLine(INVALID_INPUT);
               break;
         }
         return;
      }
}
