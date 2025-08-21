CREATE DATABASE library_management_system;
USE library_management_system;

CREATE TABLE books (
    ID INT PRIMARY KEY AUTO_INCREMENT, 
    title VARCHAR(100) NOT NULL, 
    Author VARCHAR(150) NOT NULL,
    Genre VARCHAR(50),
    Price DECIMAL(10,2),
    CHECK (Price > 0),
    PublishedYear YEAR DEFAULT 2025
);

CREATE TABLE members (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(10),UNIQUE
);

CREATE TABLE transactions (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT,
    MemberID INT,
    IssueDate DATE,
    ReturnDate DATE,
    FineAmount DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY(BookID) REFERENCES books(ID),
    FOREIGN KEY(MemberID) REFERENCES members(ID)
);
