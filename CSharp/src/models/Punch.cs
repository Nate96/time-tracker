namespace TimeTrackerModels
{
    class Punch
    {
        public int id         { get; }
        public string type    { get; }
        public string date    { get; }
        public string time    { get; }
        public string comment { get; }

        public Punch(int id, string type, string date, string time, string comment)
        {
            this.id      = id;
            this.type    = type;
            this.date    = date;
            this.time    = time;
            this.comment = comment;
        }

        ///<summary>Punch in string format</summary>
        ///<returns>
        ///Punch in the following format
        ///"Date: {} Time: {} type comment: {}
        public override string ToString()
        {
            return $"DATE: {this.GetDayOfWeek(this.date)} {this.date} {this.time} {this.type} COMMENT: {this.comment}";
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
