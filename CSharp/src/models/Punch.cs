namespace TimeTrackerModels
{
    class Punch
    {
        public int id             { get; }
        public string type        { get; }
        public DateTime punchDate { get; }
        public string comment     { get; }

        private const string DATE_TIME_FORMAT = "dddd dd-MM-yyyy hh:mm tt";

        public Punch(int id, string type,  DateTime punchDate, string comment)
        {
            this.id        = id;
            this.type      = type;
            this.punchDate = punchDate;
            this.comment   = comment;
        }

        ///<summary>Punch in string format</summary>
        ///<returns>
        ///Punch in the following format
        ///"Date: {} Time: {} type comment: {}
        public override string ToString()
        {
            return $"PUNCH: {this.punchDate.ToString(DATE_TIME_FORMAT)} {this.type} COMMENT: {this.comment}";
        }

        ///<summary>Get name of the day</summary>
        ///<returns>day of the week</returns>
        private string GetDayOfWeek(string date)
        {
            DayOfWeek day = DateTime.Parse(date).DayOfWeek;
            return $"{day}";
        }
    }
}
