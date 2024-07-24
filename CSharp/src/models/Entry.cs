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

        private const string TOP    = "---Entry---\n";
        private const string BOTTOM = "\n---End---\n";
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

        /// <summary>Entry Object to String</summary>
        /// <returns>
        /// String: Entry with the following Format
        /// ---Entry---
        /// DATE {} IN: {} OUT: {}a
        /// COMMENT:
        /// {}
        /// ---End---
        /// </returns>
        public override string ToString()
        {
            return $"{TOP}{this.inPunch.DayOfWeek} {this.inPunch.ToString(DATE_TIME_FORMAT)} - {this.outPunch.ToString(TIME_FORMAT)}, {Math.Round(this.totalTime, 2)} HOURS\nCOMMENT:\n{this.taskName}\n{this.taskComment}{BOTTOM}";
        }

        ///<summary>Formats Entry to Markdown Format</summary>
        ///<returns> String: Entry with the following Format
        ///**Date:** {} **IN:** {} **OUT:** {}
        ///**Total Time:** {} 
        ///**Comment:**
        ///{}
        ///</returns>
        public string MarkdownFormat()
        {
            //return $"{TOP}{this.GetDayOfWeek(this.date)} {this.date}, {this.timeIn} - {this.timeOut}, {this.totalTime} **HOURS:** \n**COMMENT:**\n{this.comment}{BOTTOM}";
            return "not implemented yet";
        }
    }
}
