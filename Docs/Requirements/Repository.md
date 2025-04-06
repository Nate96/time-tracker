## Connect to the Database
The system shall connect to a SQLite database defined by [CONFIG]

## Get Last Punch
If there are no punches then return a [[Defs#Punch]] with and id of -1 Else
Returns the most recent [[Defs#Punch]]

## Add Punch
Adds a [[Defs#Punch]] with the givin type and comment to the database.
Returns true when add is success
Returns false when add failed

## Add Entry
Adds [[Defs#Entry]] to the database.
Returns true if success
returns false if failed

## Get Entries
Returns a list of entries for [Valid durations]. When not given a [Valid Duration]
return and empty list
