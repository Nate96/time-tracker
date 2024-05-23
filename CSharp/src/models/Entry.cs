namespace TimeTrackerModels {
  class Entry {
    public int id { get; }
    public string  date { get; }
    public string timeIn { get; }
    public string timeOut { get; }
    public string comment { get; }
    public float totalTime { get; }

    public Entry(int id, string date, string timeIn, string timeOut, float totalTime, string comment) {
      this.id = id;
      this.date = date;
      this.timeIn = timeIn;
      this.timeOut = timeOut;
      this.comment = comment;
      this.totalTime = totalTime;
    }
  }
}
