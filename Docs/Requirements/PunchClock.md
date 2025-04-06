> This compement is responsible creating [[Defs#Punch]] and [[Defs#Entry]]
> For the System.

================================================================================
# Punch In
When the most recent [[defs#Punch]] type is "out" the system will;
Create a [[Defs#Punch]] with the following;
int:      id  
string:   "in"  
datetime: [[Defs#datetime]]  
string:   comment  
then return 1
otherwise: when the most recent [[defs#Punch]] type is "in" the system will
return 0
otherwise: when the system can't connect to a database the system will return -1


# Punch Out
When the most recent [[Defs#Punch]] type is "in" the system will;
1.  Add a [[Defs#Punch]] to the database with the following;
    int:      id  
    string:   "out"  
    datetime: [[Defs#datetime]]  
    string:   comment  
2. Add an [[defs#Entry]] to the database
3. return 1
otherwise: when the most [[defs#Punch]] type is "out" the system will return
0
otherwise: when the system can't connect to the database will return -1


# Reset > NOT IMPLEMENTED
When the most recent [[defs#Punch]] type is "in", the system will delete the
most recent [[defs#Punch]].  
otherwise: when the most recent [[defs#Punch]] is "out" return 0
otherwise: when the system can't connect to the database will return -1


# Update > NOT IMPLEMENTED
When the most recent [[defs#Punch]] type is "in", the system will update the 
most recent [[defs#Punch]] datetime with the datetime that is was given.
