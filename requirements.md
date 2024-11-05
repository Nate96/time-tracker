# Glossary

## Behind
When the user's week hours total is less than [[#Ideal hour rate]]


## Ahead
When the user's week hours total is greater than [[#Ideal hour rate]]


## Ideal hour rate
total hours = work day hours * day of the week
workd day hours = 8

40 = 8 * 5 Friday  
32 = 8 * 4 Thursday  
24 = 8 * 3 Wednesday  
16 = 8 * 2 Tuesday  
 8 = 8 * 1 Monday  


## can_punch_in
- true when the most recent [[#Punch]].type = "out"  
- false when the most recent [[#Punch]].type = "in"  


## can_punch_out
- true when the most recent [[#Punch]].type = "in"  
- false when the most recent [[#Punch]].type = "out"  
- false when there are no punches in the database  


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

# Requirements

## Req1:
When {i "some text"} is inputted and [[#can_punch_in]] = true. The System will;  
1. create a punch  
2. print "Successfully punched in"  
3. print the most recent punch in the database    


## Req2:
When {i "some text"} is inputted and [[#can_punch_in]] = false. The System will
print "Already Punched In"  


## Req3: 
When {o "some text"} is inputted and [[#can_punch_out]] = true. The System will;  
1. create new punch  
2. create a new entry  
3. print "Successfully punched out"  
4. print the most recent entry in the database  


## Req4: 
When {o "some text"} is inputted and [[#can_punch_out]] = false. The System will;  
1. NOT create a new punch  
2. NOT create a new entry   
3. print "Already Punched out" if the last [[#Punch]] type is "out"  
4. print "There are no Entries" if the Entry table is empty  


## Req5:
When {status} is inputted. The system will;  
1. print "No Punches" if there are no punches in the database  
2. print most recent [[#Punch]] from the database if the type is "in"  
3. print the most recent [[#Entry]] from the database when the most  
   recent Currently clocked out  
4. Calculates the total hours work for the current day and the current week per  
   [[#Req12:]]  
5. prints the results in the following format  
   Day:  {} hours  
   Week: {} hours "-/+"{} hours   


## Req6:
When {report} is inputted. The system shall calculate total hours for each day   
of the week and the total hours worked for the week. The system shall print the  
results in the following format.  
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


## Req7:
The system will print a [[#Punch]] in the following format  
{day of week} {date}{time AM/PM} {type}: {comment}  


## Req8:
The system will print a [[#Entry]] in the following format  
--Entry--   
{day of week} {date}{in time AM/PM} - {out time AM/PM} Hours  
{title}  
{comment}  
---End---  


## Req9:
When {report "task name"} is inputted, The system will calculate the total  
hours spent on the "task name"  


## Req10:
All datetime will be the user's local time  


## Req11:
The first day of the week is Monday  


## Req12:
When the system calculates the total week hours. The system will show if the   
user is [[#Behind]] or [[#Ahead]] by adding it to the end of the calculated total.  

#TODO Research, Implement, test
# Req13:
The system shall create a [[#Entry]] with adjusted time for daylight savings  

#TODO Research, Implement, test  
# Req14:
When a [[#Punch]] with type in is start 1/1/1 11:59 pm   
[[#Punch]] with a type out is and with time 1/1/2 12:00 am  

Create [[#Entry]] that is has a total time of 1 min  

#TODO Research, Implement, test  
## Req15:  
When {flightTest} is entered the system shall perform tests on the system to   
ensure entagraty of the system and prints out the results.  
