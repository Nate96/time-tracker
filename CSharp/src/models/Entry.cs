namespace TimeTrackerModels
{
    class Entry
    {
        public int       id          { get; }
        public DateTime  inPunch     { get; }
        public DateTime  outPunch    { get; }
        public float     totalTime   { get; }
        public  string   taskName    { get; }
        public  string   taskComment { get; }

        private const string DATE_TIME_FORMAT = "dddd dd-MM-yyyy hh:mm tt";
        private const string TIME_FORMAT = "hh:mm tt";

        public Entry(int id, DateTime inPunch, DateTime outPunch, float totalTime, string taskName, string taskComment)
        {
            this.id          = id;
            this.inPunch     = inPunch;
            this.outPunch    = outPunch;
            this.totalTime   = totalTime;
            this.taskName    = taskName;
            this.taskComment = taskComment;
        }

        /// <summary>
        ///    <para/> Entry Object to String
        ///    <para/>  ==== Entry ====
        ///    <para/> Day, Date, timeIn - timeOut, totalHours
        ///    <para/> Title:   ""
        ///    <para/> Comment: ""
        /// </summary>
        /// <returns>
        ///    string
        /// </returns>
        public override string ToString()
        {
            return $"=== Entry ===\n"
                 + $"{this.inPunch.ToString(DATE_TIME_FORMAT)} - {this.outPunch.ToString(TIME_FORMAT)}, {Math.Round(this.totalTime, 2)} HOURS\n"
                 + $"Title:   {this.taskName}\n"
                 + $"Comment: {this.taskComment}\n";
        }

        public string MarkdownFormat()
        {
            return "not implemented yet";
        }
    }
}
