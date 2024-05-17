using RepositoryNameSpace;

class Program
{
  static void Main(string[] args)
  {
    if (args.Length != 3)
    {
      Console.WriteLine("Usage: TimeLogger <InTime> <OutTime> <Message>");
      return;
    }

    string InTime = args[0];
    string OutTime = args[1];
    string Comment = args[2];

    Console.WriteLine(InTime);
    Console.WriteLine(OutTime);
    Console.WriteLine(Comment);

    // Initialize database
    //DatabaseHelper.InitializeDatabase();

    // Save the log
    //DatabaseHelper.SaveTimeLog(inTime, outTime, message);

    Console.WriteLine("Time log saved successfully.");

    Repository repository = new Repository();
  }
}
