CREATE database LIBRARY_MANAGEMENT_SYSTEM;
USE LIBRARY_MANAGEMENT_SYSTEM;
CREATE TABLE Books (
ID int PRIMARY KEY AUTOINCREMENT, 
title varchar(50) not null, 
Author varchar(150) not null,
Genre varchar(50),
Price int,
check (Price > 0),
PublisedYear year DEFAULT 2025
);

CREATE TABLE Members (
ID int not null PRIMARY KEY AUTOINCREMENT
FirstName varchar(50) not null,
LastName varchar(50) not null,
Email varchar(50) UNIQUE,
Phone VARCHAR(10)
);

CREATE TABLE Transactions (
ID int PRIMARY KEY AUTOINCREMENT,
BookID int ,
MemberID int ,
IssueDate date,
ReturnDate date,
FineAmount INT DEFAULT 0,
FOREIGN KEY(ID) REFERENCES Books(ID),
FOREIGN KEY(ID) REFERENCES Members(ID)
)