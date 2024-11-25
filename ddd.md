©2015 Documentation Consultants (www.SDLCforms.com)   

Project Name - Time Tracker  
Version ------ 1.0  

# 1 Purpose
The Database Design Document maps the logical data model to the target database
management system with consideration to the system’s performance requirements.
The Database Design converts logical or conceptual data constructs to physical
storage constructs (e.g., tables, files) of the target Database Management
System (DBMS).

## 1.1 Document Objectives
The Database Design Document has the following objectives:
- To describe the design of a database, that is, a collection of related data
  stored in one or more computerized files that can be accessed by users or
  computer developers via a DBMS.
- To serve as a basis for implementing the database and related software units.
  It provides the acquirer visibility into the design and provides information
  necessary for software development.

## 1.2 Intended Audience
This document is intended for the following audiences:
- Technical reviewers, who must evaluate the quality of this document.
- Developers including:
    - Architects, whose overall architecture design must meet the requirements
      specified in this document.
    -  Designers, whose design must meet the requirements specified in this
       document.
    - Developers, whose software must implement the requirements specified in
      this document.
    - Quality Assurance personnel, whose test cases must validate the
       requirements specified in this document.

## 1.3 Acronyms and Abbreviations
RDMS - Relational Database Management System  
DBA -- Database Administrator  

## 1.4 Key Personnel
1. self 

## 1.5 Data Owners
1. self


# 2 Assumptions, Constraints and Dependencies  

##  2.1 Assumptions  
Describe any assumptions that influence the database design.  

## 2.2 Constraints  
1. Database must be stored locally  
2. Must not must any ports  

## 2.3 Dependencies
Dependencies that impact the database design such as related hardware, software,
or operating systems.
1. Windows
2. MacOS
3. Ubuntu
4. SQLite


# 3 System Overview
Clock in and Clock out application

## 3.1 Database Management System Configuration
SQLite Cli - [https://www.sqlite.org/cli.html]  

To perform queries on datbase perform the following SQLite command in terminal
in the current directory.
```bash
sqlite3 log.db < {my-sql-file} > results.txt
```

## 3.2 Database Software Utilities
Any text editor

## 3.3 Support Software
None


# 4 Architecture

## 4.1 Hardware Architecture
None

## 4.2 Software Architecture
layer Architecture: cli <> Business Logic <> Database

## 4.3 Datastores  
None

# 5 Database-Wide Design Decisions
How the Database will behave form a user’s viewpoint in meeting its
requirements, ignoring internal implementation, and other decisions affecting
the design of the database.

## 5.1 Key Factors Influencing Design
1. Database must be stored locally  
2. Must not must any ports  

## 5.2 DBMS Platform
Recommended OS is Linux or MacOs. The software can also work on windows, but
note SQLite CLI does not work on windows. Need to read powerscript documentation
to run sql scripts on the database.

## 5.3 Security and Availability
There is only one user in the databse. All access to the data is managed by the
system's security proticals.


## 5.4 Distribution
None

## 5.5 Backup and Restore Operations
None

## 5.6 Performance and Availability Decisions
Discuss how performance and availability requirements will be met.


# 6 Database Administrative Functions

## 6.1 Responsibility
Identify the organizations and personnel responsible for the database
administration functions:
- database administrator
- system administrator
- security administrator

## 6.2 Database Identification
File Location: ./Log.db

## 6.5 Schema Information
Describe the overall structure of the schema and other global definition of the
database.

## 6.6 Schema Description
Punch Table
```sql
CREATE TABLE IF NOT EXISTS  punch(
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
   , type TEXT NOT NULL CHECK(type IN ('out', 'in'))
   , punch_date DATETIME NOT NULL
   , comment TEXT NOT NULL
);
```

Entry Table
```sql
CREATE TABLE IF NOT EXISTS entry(
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
   , in_punch DATETIME NOT NULL
   , out_punch DATETIME NOT NULL
   , total_time FLOAT NOT NULL
   , task_name TEXT NOT NULL
   , task_comment TEXT NOT NULL
);
```

## 6.15 Storage   
As much as you give it  

## 6.16 Backup and Recovery
None
