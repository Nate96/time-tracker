namespace TimeTrackerModels
{
    class Entry
    {
        public int id          { get; }
        public string date     { get; }
        public string timeIn   { get; }
        public string timeOut  { get; }
        public string comment  { get; }
        public float totalTime { get; }

        private const string TOP    = "---Entry---\n";
        private const string BOTTOM = "\n---End---\n";

        public Entry(int id, string date, string timeIn, string timeOut, float totalTime, string comment)
        {
            this.id = id;
            this.date = date;
            this.timeIn = timeIn;
            this.timeOut = timeOut;
            this.comment = comment;
            this.totalTime = totalTime;
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
            return $"{TOP}{this.GetDayOfWeek(this.date)} {this.date}, {this.timeIn} - {this.timeOut}, {this.totalTime} HOURS\nCOMMENT:\n{this.comment}{BOTTOM}";
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
            return $"{TOP}{this.GetDayOfWeek(this.date)} {this.date}, {this.timeIn} - {this.timeOut}, {this.totalTime} **HOURS:** \n**COMMENT:**\n{this.comment}{BOTTOM}";
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
