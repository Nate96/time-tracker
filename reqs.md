# Req1:
When {i "some text"} is inputted and [[reqs#can_punch_in]] = true. The System
will create a punch and prints the most recent punch 


# Req2:
When {i "some text"} is inputted and [[reqs#can_punch_in]] = false. The System
will print "Already Punched In"


# Req3: 
When { o "some text"} is inputted and [[reqs#can_punch_out]] = true. The System
will print the most recent entry in the database


# Req4: 
When { o "some text"} is inputted and [[reqs#can_punch_out]] = false. The System
will print "There are no Entries in the database" when there is not entries in 
the database or print "Already punched out when the most recent punch type is out"


# Req5:
When { status } is inputted.
- The system will print "No Punches" when there is not punches in the database
- When the most recent punch type is "in" the system will print;
{most_recent_punch}

Day:  {}
Week: {}
- When the most recent punch type is "out" the system will print
Currently clocked out

Day:  {}
Week: {}


# Req6
When { report } is inputted. The system shall print
v---------------------
Monday:     {} hours
Tuesday:    {} hours
Wednesday:  {} hours
Thursday:   {} hours
Friday:     {} hours
Saturday:   {} hours
Sunday:     {} hours
v---------------------
Total:      {} hours

NOTE: Ignore v it is for formatting


# can_punch_in
true when the most recent punch type is "out"
false when the most recent punch type is "in"

# can_punch_out
true when the most recent punch is "in"
false when themost recent punch is "out" or there are not punches in the databse
