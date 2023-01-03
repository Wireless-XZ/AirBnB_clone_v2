-- a script that prepares a MySQL server for the project:
CREATE IF NOT EXISTS DATABASE hbnb_db;
CREATE IF NOT EXISTS USER 'hbnb'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT * ON hbnb_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema TO 'hbnb'@'localhost';
