# Glossary  

## Punch
int:      id  
string:   type "in" or "out"  
datetime: punch datetime  
string:   comment  


## Entry
int:      id  
datetime: in punch
datetime: out punch  
float:    total time  
string:   task name  
string:   task comment  


## Ideal hour rate  
total hours = work day hours * day of the week  
workd day hours = 8  

40 = 8 * 5 Friday  
32 = 8 * 4 Thursday  
24 = 8 * 3 Wednesday  
16 = 8 * 2 Tuesday  
 8 = 8 * 1 Monday  


## can_punch_in  
A boolean varible that determins if a [[#Punch]] with a type of "in" can be added  
to the database  


## can_punch_out  
A boolean varible that determins if a [[#Punch]] with a type of "out" can be  
added to the database


## datetime:
All datetime will be local time  


## fist day of the week:
The first day of the week is Monday  


# Requirements

## Req1:
When {i "some text"} is inputted and [[#can_punch_in]] is true. The System shall;  
1. create a [[#Punch]] in the database
2. print "Successfully punched in"  
3. print the most recent [[#Punch]] in the database  
otherwise
print "Already Punched In"


## Req2: 
When {o "some text"} is inputted and [[#can_punch_out]] is true. The System shall;  
1. create new punch in the database  
2. create a new entry in the database  
3. print "Successfully punched out"  
4. print the most recent entry in the database  
otherwise
print "Already Punched out"


## Req3: 
When {o "some text"} is inputted and [[#can_punch_out]] = false. The System will;  
1. if the last [[#Punch]] type is "out" print "Already Punched out"   
2. if the Entry table is empty print "There are no Entries"   


## Req4:
When "status" is inputted and there are [[#Punch]]s in the database the system 
shall print "no punches"


## Req5:
When "status" is inputted and the most recent [[#Punch]]'s type is "in" the  
system shall print the most recent [[#Punch]].  


## Req6:
When "status" is inputted and the most recent [[#Punch]]'s type is "out" the 
system shall;
1. print "currently clocked out"
2. Calculate the sum of hours work for the current day and the current week  
3. [[#Req9:]]
5. prints the results in the following format  
   Day:  {} hours  
   Week: {} hours "-/+"{}  


## Req7:
When "report" is inputted. The system shall calculate;
1. Total hours for each day the week
2. The total hours worked for the week.

The system shall print the  results in the following format.  
v---------------------  
Monday:     {} hours  
Tuesday:    {} hours  
Wednesday:  {} hours  
Thursday:   {} hours  
Friday:     {} hours  
Saturday:   {} hours  
Sunday:     {} hours  
v---------------------   
Total:      {} hours "-/+"{}

NOTE: Ignore v it is for formatting  


## Req8:
The system shall print a [[#Punch]] in the following format;  
{day of week} {date}{time AM/PM} {type}: {comment}  


## Req9:
The system will print a [[#Entry]] in the following format;  
--Entry--   
{day of week} {date}{in time AM/PM} - {out time AM/PM} Hours  
{title}  
{comment}  
---End---  


## Req10:
The systam shall calculate the difference between the sum of hours for the
current week and the [[#Ideal hour rate]] for the current day
 

## Req11:
When "help" is entered. The system shall print the title and how to use
section in [[README]] to the terminal.


## Req12:
When the last [[#Punch]] type is "out" the system shall set [[#can_punch_in]]
to true. Otherwise the system shall set [[#can_punch_in]] to false.


## Req13:
When the last [[#Punch]] type is "out" or there are no [[#Punch]]s in the databse
the system shall set [[#can_punch_out]] to false otherwise the system shall set
[[#can_punch_out]] to true


#TODO Research, Implement, test
# Req13:
The system shall create a [[#Entry]] with adjusted time for daylight savings  

#TODO Research, Implement, test  
# Req1:
When a [[#Punch]] with type in is start 1/1/1 11:59 pm   
[[#Punch]] with a type out is and with time 1/1/2 12:00 am  

Create [[#Entry]] that is has a total time of 1 min  

#TODO Research, Implement, test  
## Req15:  
When {flightTest} is entered the system shall perform tests on the system to   
ensure entagraty of the system and prints out the results.

#TODO: Research, Implement, test
## Req11:
When {report "task name"} is inputted, The system will calculate the total  
hours spent on the "task name"  
