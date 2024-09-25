# Req1:
When {i "some text"} is inputted and [[reqs#can_punch_in]] = true. The System
will;
1. create a punch
2. print " Sucessfully punched in"
3. print the most recent punch in the database


# Req2:
When {i "some text"} is inputted and [[reqs#can_punch_in]] = false. The System
will print "Already Punched In"


# Req3: 
When { o "some text"} is inputted and [[reqs#can_punch_out]] = true. The System
will;
1. create new punch
2. create a new entry
3. print "Seccessfully punched out"
4. print the most recent entry in the database


# Req4: 
When { o "some text"} is inputted and [[reqs#can_punch_out]] = false. The System
will;
1. NOT create a new punch
2. NOT create a new entry 
3. print "Already Punched out" if the last [[reqs#Punch]] type is "out"
4. print "There are no Entries" if the Entry table is empty


# Req5:
When { status } is inputted. The system will;
1. print "No Punches" if there is not punches in the database
2. print most recent [[reqs#Punch]] from the database if the type is "in"
3. print the most recent [[reqs#Entry]] from the database when the most recent
   Currently clocked out
4. Caluclates the total hours work for the current day and the current week per
   [[reqs#Req12:]]
5. prints the results in the following format
   Day:  {} hours
   Week: {} hours "-/+"{} hours 


# Req6:
When { report } is inputted. The system shall calulate total hours for each day 
of the week and the total hours worked for the week. The system shall print the
results in the following formate.
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


# Req7:
The system will print a [[reqs#Punch]] in the following formate
{day of week} {date}{time AM/PM} {type}: {comment}


# Req8:
The system will print a [[reqs#Entry]] in the following formate
--Entry-- 
{day of week} {date}{in time AM/PM} - {out time AM/PM} Hours
{title}
{comment}
---End---


# Req9:
When { report "task name" } is inputted, The system will will calculate the
total house spent on the "task name"


# Req10:
All datetime will be the user's local time


# Req11:
The first day of the week is Monday


# Req12:
When the system calculates the total week hours. The system will show if the 
user is behind or ahead hours by adding it to the end of the calulated total. 
The system will use 8 hours day for 5 days a week as the the standard rate of 
work


# can_punch_in
- true when the most recent [[reqs#Punch]].type = "out"
- false when the most recent [[reqs#Punch]].type = "in"


# can_punch_out
- true when the most recent [[reqs#Punch]].type = "in"
- false when the most recent [[reqs#Punch]].type = "out"
- flase when there are no punches in the databse


# Punch
int:      id
string:   type "in" or "out"
datetime: punch datetime
string:   comment


# Entry
int:      id
datetime: in punch
datetime: out punch
float:    total time
string:   task name
string:   task comment

