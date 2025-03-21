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


# Ideal hour rate  
total hours = work day hours * day of the week  
work day hours = 8  

40 = 8 * 5 Friday  
32 = 8 * 4 Thursday  
24 = 8 * 3 Wednesday  
16 = 8 * 2 Tuesday  
 8 = 8 * 1 Monday  


# can_punch_in  
1. When the last [[#Punch]] type is out.
2. When [[#Punch]] has NOT been created yet.


# can_punch_out  
1. When the last [[#Punch]] type is in.


# datetime:
All datetime will be local time  


# fist day of the week:
The first day of the week is Monday  


# Julian Day
Julian dates (abbreviated JD) are simply a continuous count of days and
fractions since noon Universal Time on January 1, 4713 BC
(on the Julian calendar).
