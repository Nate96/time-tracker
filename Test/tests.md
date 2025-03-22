# Invalid Input 
When {adft} is entered verifythe system prints "ERROR: Invalid input, please
refer to README.md for more information." 


# Status While No Database
When {status} is entered, verify, the system prints "ERROR: No database found."


# Punched out while No Database
When {o "test"} is entrired verify the sytsem prints "ERROR: No database found."


# Punched in while No Database
When {i "test"} is entrired verify the sytsem prints "ERROR: No database found."


# Status With no Pucnhes
When {status} is entered verify the system prints "No punches."


# Punch In  
When {i "test"} is entered. Verify the sytem;
1. A [[Defs#Punch]] with type in is added to the database
2. Print "Succesfully punched in"
3. print {current day of the week} {date} {time} tests


# Status While Punched In
When {status} is entered. verify the system prints
Punched IN for {x} hours
{current day of the week} {date} {time} tests


# Punch in while punched in
When {i "test"} is entered, Verify the system will print "ERROR: Currently 
punched in"


# Punch Out
When {o "test} is entered Verify the sytem will print;
1. A [[Defs#Punch]] with type out is added to the database 
2. An [[Defs#Entry]] is added to the database
3. Prints 
    SUCCESS: punched out
    SUCCESS: Entry added
    ==== ENTRY ====
    {current day of the week} {date} {time} tests
    Tilte:   test
    Comment: test

    DAY:  {total} hours
    WEEK: {total} hours


# Punching out while punched out 
When {o "test} in entered verify the system prints "ERROR: Currerntly punched
out"


# Status While Punched Out
When {status} is entered, verify the system prints
Currently Punched Out
==== ENTRY ====
{current day of the week} {date} {time} tests
Tilte:   test
Comment: test

DAY:  {total} hours
WEEK: {total} hours


# Report
When {report} is entered, Verify the system prints 
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
