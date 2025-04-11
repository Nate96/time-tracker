using TimeTrackerErrors;
using TimeTrackerModels;
using TimeTrackerConfig;


namespace TimeTrackerPresenter 
{
   class Presenter
   {
      /// <summary>
      ///    <para/> Returns
      ///    <para/> Punch Success Message
      ///    <para/> Entry Success Message
      ///    <para/> string of <typeparamref name="Entry"/>
      /// </summary>
      /// <returns>
      ///   string
      /// </returns>
      public static string PunchOutSuccess(string entry)
      {
         return $"{ErrorMessages.PUNCHOUT_SUCCESS}\n"
              + $"{ErrorMessages.ENTRY_SUCCESS}\n"
              + $"{entry}";
      }

      /// <summary>
      ///    <para/> Returns
      ///    <para/> Punched in for {total}
      ///    <para/> string of <typeparamref name="Punch"/>
      ///    <para/> Day:  {}
      ///    <para/> Week: {} (+/-)
      /// </summary>
      public static string InStatus(Punch punch, List<Entry> dayEntries, List<Entry> weekEntries)
      {
         TimeSpan currentTotalTime = DateTime.Now - punch.punchDate;
         
         float currentHours = Abacus.Round(((float)currentTotalTime.TotalMinutes / 60));
         float weekhours = Abacus.Round(currentHours + weekEntries.Sum(e => e.totalTime)); 
         float daySum = Abacus.Round(currentHours + dayEntries.Sum(e => e.totalTime));

         string weekLine;
         float weekdif;
         bool hasTarget = Tracker.ACTIVE;

         if (hasTarget)
         {
            weekdif = Abacus.projectedHours(weekhours);
            weekLine = $"Week: {weekhours} hours ({weekdif})\n";
         }
         else
            weekLine = $"Week: {weekhours} hours\n";

         return $"Punch in for {currentHours} hours\n"
            + punch.ToString() + "\n\n"
            + $"Day:  {daySum} hours\n"
            + weekLine;
      }

      /// <summary>
      ///    <para/> Returns
      ///    <para/> Currently Punched Out
      ///    <para/> the string of <paramref name="entry"/>
      /// </summary>
      public static string outStatus(Entry entry, List<Entry> dayEntries, List<Entry> weekEntries)
      {
         if (entry == null) return "ERROR: punches out of synce.";

         bool hasTarget = Tracker.ACTIVE;

         float weekHours = Abacus.Round(weekEntries.Sum(e => e.totalTime));
         float daySum = Abacus.Round(dayEntries.Sum(e => e.totalTime));
         
         float weekDif;
         string weekLine;

         if (hasTarget)
         {
            weekDif = Abacus.projectedHours(weekHours);
            weekLine = $"Week: {weekHours} hours ({weekDif})\n";
         }
         else
            weekLine = $"Week: {weekHours} hours\n";

         return "Currently Punched Out\n" 
            + entry.ToString()
            + $"\nDay:  {daySum} hours\n"
            + weekLine;
      }

      /// <summary>
      ///    <para/> Calculates the total hours worked for each day and week
      ///    <para/> Returns
      ///    <para/> "Monday:    {} hours"
      ///    <para/> "Tuesday:   {} hours"
      ///    <para/> "Wednesday: {} hours"
      ///    <para/> "Thursday:  {} hours"
      ///    <para/> "Friday:    {} hours"
      ///    <para/> "Saturday:  {} hours"
      ///    <para/> "Sunday:    {} hours"
      ///    <para/> -------------------------
      ///    <para/> Total:      {} hours (+/-)
      /// </summary>
      public static string reportWeekHours(List<Entry> entries)
      {
           const uint WEEK_DAY_NUMBER = 7;
           float [] weekHours = new float[WEEK_DAY_NUMBER];
           bool hasTarget = Tracker.ACTIVE;

           float difHours;
           string totalLine;

           foreach (Entry entry in entries)
           {
              //NOTE: This is to adjust for monday being the start of the week
              uint adjusted = ((uint)entry.inPunch.DayOfWeek + 6) % 7;
              weekHours[adjusted] += entry.totalTime;
           }

           float totalWeekHours = Abacus.Round(weekHours.Sum());

           if (hasTarget)
           {
              difHours = Abacus.projectedHours(totalWeekHours);
              totalLine = $"Total:     {totalWeekHours} hours ({difHours})";
           }
           else
              totalLine =  $"Total:     {totalWeekHours} hours";

           return $"Monday:    {weekHours[0]} hours\n"
                + $"Tuesday:   {weekHours[1]} hours\n"
                + $"Wednesday: {weekHours[2]} hours\n"
                + $"Thursday:  {weekHours[3]} hours\n"
                + $"Friday:    {weekHours[4]} hours\n"
                + $"Saturday:  {weekHours[5]} hours\n"
                + $"Sunday:    {weekHours[6]} hours\n"
                + "-------------------------\n"
                + totalLine;
      }

      private class Abacus 
      {
         /// <summary>
         ///   Calculates hours and shows weather the current hours is behind 
         ///   or ahead of the expected hours for the current day in the week.
         /// </summary>
         /// <param name="hours"> hours worked for the current week</param>
         public static float projectedHours(float hours)
         {
            const float DAY_AVERAGE = Tracker.TARGET_WORK_HOURS / Tracker.MAX_WORK_WEEK_DAYS;

            int currentDay = ((int)DateTime.Now.DayOfWeek);
            float projectedHours;

            if (currentDay <= Tracker.MAX_WORK_WEEK_DAYS && currentDay != 0.0)
               projectedHours = currentDay * DAY_AVERAGE;
            else
               projectedHours = Tracker.TARGET_WORK_HOURS;
            return Round(hours - projectedHours);
         }
         
         /// <summary>
         ///   round a float to two decimal points
         /// </sumary>
         public static float Round(float num) { return (float)Math.Round(num, 2); }
      }
   }
}
