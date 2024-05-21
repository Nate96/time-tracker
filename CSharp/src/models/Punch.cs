namespace TimeTrackerModels {
  class Punch {
    public int id { get; }
    public string type { get; }
    public string date { get; }
    public string time { get; }
    public string comment { get; }

    public Punch(int id, string type, string date, string time, string comment) {
      this.id = id;
      this.type = type;
      this.date = date;
      this.time = time;
      this.comment = comment;
    }
  }
}
