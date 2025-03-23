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
work day hours = x  

40 = x * 5 Friday  
32 = x * 4 Thursday  
24 = x * 3 Wednesday  
16 = x * 2 Tuesday  
 8 = x * 1 Monday  

## Can Punch In  
1. When the last [[#Punch]] type is out.
2. When [[#Punch]] has NOT been created yet.

## Can Punch Out  
When the last [[#Punch]] type is in.

## datetime:
All datetime will be local time  

## fist day of the week:
The first day of the week is Monday  

## Julian Day
Julian dates (abbreviated JD) are simply a continuous count of days and
fractions since noon Universal Time on January 1, 4713 BC
(on the Julian calendar).

## Track
I boolean value that is set by the user via [CONFIG]
