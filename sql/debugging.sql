ALTER TABLE members MODIFY ID INT NOT NULL AUTO_INCREMENT;


INSERT INTO members (FirstName, LastName, Email, Phone)
VALUES ('Test', 'User', 'testuser@example.com', '0123456789');

SELECT * FROM members ORDER BY ID DESC;
