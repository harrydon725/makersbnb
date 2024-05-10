-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.
-- First, we must delete (drop) all our tables
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS spaces CASCADE;
DROP TABLE IF EXISTS bookings;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP SEQUENCE IF EXISTS spaces_id_seq;
DROP SEQUENCE IF EXISTS bookings_id_seq;
-- drop sequences and tables
-- create sequence and table
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email_address VARCHAR(255),
    password VARCHAR(255)
);
-- create sequence and table
CREATE SEQUENCE IF NOT EXISTS spaces_id_seq;
CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    price DECIMAL(5, 2),
    start_date DATE,
    end_date DATE,
    ownerID INTEGER,
    CONSTRAINT fk_ownerID FOREIGN KEY (ownerID) REFERENCES users(id) ON DELETE CASCADE
);
-- create sequence and table
CREATE SEQUENCE IF NOT EXISTS bookings_id_seq;
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    booking_date DATE,
    userID INTEGER,
    spaceID INTEGER,
    CONSTRAINT fk_spaceID FOREIGN KEY (spaceID) REFERENCES spaces(id) ON DELETE CASCADE,
    CONSTRAINT fk_userID FOREIGN KEY (userID) REFERENCES users(id) ON DELETE CASCADE
);
-- Finally, we add any records that are needed for the tests to run
INSERT INTO users (email_address, password) VALUES ('matthew@gmail.com', '$2b$12$wuVZ7gFuaWwfeB8OdBsow.DrjAt30msLYkRMTlnSYZdhE5/Uwzp4.');
INSERT INTO users (email_address, password) VALUES ('myrto@hotmail.com', '6789@Gkx');
INSERT INTO users (email_address, password) VALUES ('constantine@smith.net', 'Password123!');
INSERT INTO users (email_address, password) VALUES ('john@yahoo.com', 'Hello67£');
INSERT INTO users (email_address, password) VALUES ('alice@mail.com', 'Fdfdfd21$');
INSERT INTO spaces (title, price, start_date, end_date, ownerID) VALUES ('Studio apartment', 100, '2024-05-20', '2025-05-20', 1);
INSERT INTO spaces (title, price, start_date, end_date, ownerID) VALUES ('3 bedroom flat', 250, '2024-05-10', '2024-12-10', 2);
INSERT INTO spaces (title, price, start_date, end_date, ownerID) VALUES ('Penthouse', 500, '2024-05-25', '2026-05-25', 3);
INSERT INTO spaces (title, price, start_date, end_date, ownerID) VALUES ('Town house', 180, '2024-06-25', '2026-10-28', 3);
INSERT INTO bookings (booking_date, userID, spaceID) VALUES ('2024-06-10', 4, 1);
INSERT INTO bookings (booking_date, userID, spaceID) VALUES ('2024-05-12', 5, 2);
INSERT INTO bookings (booking_date, userID, spaceID) VALUES ('2024-06-10', 1, 3);
INSERT INTO bookings (booking_date, userID, spaceID) VALUES ('2026-10-28', 2, 4);

