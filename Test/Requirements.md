# REC1 1 - [[README#How to use]]
Let A = [[Glossary#punch]] with the maximum datetime in database. 
[[Glossary#punch]] with a type of "in" can only be created when [[Requirements#REC2]]
is satisfied and either of the following conditions are met:
1. there are no punches in the database
2. A.type == "in"
Otherwise print [[Glossary#DATABASE_INVALID_STATE]]

# REC2
A valid input to create a punch is i "somestring". Replace somestring with any
string you want. NOTE this will be the Title of the entry. Otherwise print
[[Glossary#INVALID_INPUT]]

# REC4 2-[[README#How to use]] 
A [[Glossary#punch]] shall be created when a valid input defined in
[[Requirements#REC3]] is given and the database is in a valid state definded in
[[Requirements#REC2]]
Otherwise Print [[Glossary#ADD_PUNCH_ERROR]] and a new [[Glossary#punch]] is not
created






# TC1
When {i "test title"} is entered, verify [punch] is created in the defined
databse when [[Requirements#REC1]] is satifided

# TC2
When [REC1] is NOT satisfied and {i "test title"} is entered, verify [[punch]]
is NOT created in the database and A INVALID_STATE is printed



'''H2-TC2:
When {o "test comment about entry"} is entered, verify [[punch]] and [[entry]]
is created in the defined database
'''

# TEST CASES:


# GLOSSARY
1.
2.
3.

