namespace TimeTrackerConfig 
{
   public static class DbConfig
   {
      public const string ABSOLUTE_PATH = "";

      public const string DATABASE_LOCATION = ABSOLUTE_PATH + "/Log.db";
      public const string CREATE_TABLE      = ABSOLUTE_PATH + "/SqlScripts/CreateTables.sql";
      public const string LAST_PUNCH        = ABSOLUTE_PATH + "/SqlScripts/GetLastPunch.sql";
      public const string INSERT_PUNCH      = ABSOLUTE_PATH + "/SqlScripts/InsertPunch.sql";
      public const string INSERT_ENTRY      = ABSOLUTE_PATH + "/SqlScripts/InsertEntry.sql";
      public const string TODAY             = ABSOLUTE_PATH + "/SqlScripts/GetTodayEntry.sql";
      public const string WEEK              = ABSOLUTE_PATH + "/SqlScripts/GetWeekEntry.sql";
      public const string MONTH             = ABSOLUTE_PATH + "/SqlScripts/GetMonthEntry.sql";
      public const string LAST_ENTRY        = ABSOLUTE_PATH + "/SqlScripts/GetLastEntry.sql";
   }

   public static class Tracker
   {
      public const int TARGET_WORK_HOURS = 5;
      public const int MAX_WORK_WEEK_DAYS = 5;
      public const bool ACTIVE  = false;
   }
}
