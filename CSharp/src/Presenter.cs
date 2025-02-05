using TimeTrackerErrors;
using TimeTrackerModels;
using TimeTrackerConfig;


namespace TimeTrackerPresenter 
{
   class Presenter
   {
      public string PunchOutSuccess(string entry)
      {
         return $"{ErrorMessages.PUNCHOUT_SUCCESS}\n"
              + $"{ErrorMessages.ENTRY_SUCCESS}\n"
              + $"{entry}";
      }

      public string InStatus(Punch punch, List<Entry> dayEntries, List<Entry> weekEntries)
      {
         TimeSpan currentTotalTime = DateTime.Now - punch.punchDate;
         
         float currentHours = (float)Math.Round(((float)currentTotalTime.TotalMinutes / 60), 2);
         float weekhours = currentHours + weekEntries.Sum(e => e.totalTime); 
         float daySum = currentHours + dayEntries.Sum(e => e.totalTime);

         string weekLine;
         float weekdif;
         bool hasTarget = Hours.ACTIVE;

         if (hasTarget)
         {
            weekdif = projectedHours(weekhours);
            weekLine = $"Week: {weekhours} hours ({weekdif})\n";
         }
         else
            weekLine = $"Week: {weekhours} hours\n";

         return $"Punch in for {currentHours} hours\n"
            + punch.ToString() + "\n\n"
            + $"Day:  {daySum} hours\n"
            + weekLine;
      }

      public string outStatus(Entry entry, List<Entry> dayEntries, List<Entry> weekEntries)
      {
         if (entry == null) return "ERROR: punches out of synce.";

         float weekHours = weekEntries.Sum(e => e.totalTime);
         float daySum = dayEntries.Sum(e => e.totalTime);
         
         float weekDif;
         string weekLine;
         bool hasTarget = Hours.ACTIVE;

         if (hasTarget)
         {
            weekDif = projectedHours(weekHours);
            weekLine = $"Week: {weekHours} hours ({weekDif})\n";
         }
         else
            weekLine = $"Week: {weekHours} hours\n";

         return "Punched Out\n" 
            + entry.ToString()
            + $"Day:  {daySum} hours\n"
            + weekLine;
      }

      public string reportWeekHours(List<Entry> entries)
      {
           const uint WEEK_DAY_NUMBER = 7;
           float [] weekHours = new float[WEEK_DAY_NUMBER];

           foreach (Entry entry in entries)
           {
              //NOTE: This is to adjust for monday being the start of the week
              uint adjusted = ((uint)entry.inPunch.DayOfWeek + 6) % 7;
              weekHours[adjusted] += entry.totalTime;
           }

           double totalWeekHours = weekHours.Sum();
           float difHours;
           string totalLine;
           bool hasTarget = Hours.ACTIVE;

           if (hasTarget)
           {
              difHours = projectedHours((float)totalWeekHours);
              totalLine = $"Total:     {weekHours.Sum()} hours ({difHours})";
           }
           else
              totalLine =  $"Total:     {weekHours.Sum()} hours";


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

      private float projectedHours(float hours)
      {
         const float DAY_AVERAGE = Hours.TARGET_WORK_HOURS / Hours.MAX_WORK_WEEK_DAYS;

         int currentDay = ((int)DateTime.Now.DayOfWeek);
         float projectedHours;

         if (currentDay <= Hours.MAX_WORK_WEEK_DAYS)
            projectedHours = (float)Math.Round(currentDay * DAY_AVERAGE, 2);
         else
            projectedHours = Hours.TARGET_WORK_HOURS;

         return (float)Math.Round(hours - projectedHours, 2);
      }
   }
}
