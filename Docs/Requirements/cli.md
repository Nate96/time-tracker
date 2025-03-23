> Interface is responsible for inputs from the user VIA command line and
> outputs. These Requirements WILL NOT reference Logic/computation done by
> other components of the System.

===============================================================================
## Punch In
When "i {string}" is inputted and [[Defs#Can Punch In]] is true.
The System will;
1. create a [[Defs#Punch]]  
2. print [[Messages#Punch In Success]]  
3. print the most recent [[Defs#Punch]]  
otherwise When [[Defs#Can Punch In]] is false
print [[Messages#Can't Punch In]] 


## Punch Out
When "o {string}" is inputted and [[Defs#Can Punch Out]] is true. The System
will;  
1. [[PunchClock#Punch Out]]
2. [[PunchClock#Create Entry]]
3. print [[Messages#Punch Out Success]]  
4. print the most recent entry in the database  
otherwise when [[Defs#Can Punch Out]] is false
print [[Messages#Can't Punch Out]]


## Status
### Status With no Pucnhes 
When "status" is inputted and there are no [[Defs#Punch]], the system will
print "no punches"

### Status While Punched In
When "status" is inputted and the most recent [[Defs#Punch]] type is "in"
the system will print the most recent [[Defs#Punch]].
1. Print "Punched in for {x} Hours"
2. Print most resent [[Defs#Punch]] \n\n
3. print "Day:  {total worked hours for current day} hours"
4. print "Week: {total worked hours for the current week}" hours"

### Status While Punched Out
When "status" is inputted and the most recent [[Defs#Punch]] type is "out"
the system will;
1. print "currently clocked out"
2. Print an [[Defs#Entry]] 
3. Prints the results in the following format  
   Day:  {total} hours  
   Week: {total} hours "-/+"{total}  


## Report
When "report" is inputted. The system will calculate;
1. Total hours for each day the week
2. The total hours worked for the week.

The system shall print the  results in the following format.  
>---------------------  
Monday:     {total} hours  
Tuesday:    {total} hours  
Wednesday:  {total} hours  
Thursday:   {total} hours  
Friday:     {total} hours  
Saturday:   {total} hours  
Sunday:     {total} hours  
>---------------------   
Total:      {total} hours "-/+"{total}


## Update Last Punch > NOT IMPLEMENTED
When "update {[[Defs#DateTime]]" unputted and the last [[Defs#Punch]]
type is "in". The system will;
1. Print last [[Defs#Punch]]
2. Update the last punch to the inputted [[Defs#DateTime]].
3. Print updated punch [[Defs#DateTime]]
otherwise
print "currently clocked out"
