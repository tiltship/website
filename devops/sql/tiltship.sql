CREATE DATABASE tiltship;

CREATE TABLE tiltship.signups(
       email VARCHAR PRIMARY KEY CHECK (email != ''),
       tracking_data JSON NOT NULL CHECK (tracking_data != 'null'::json)
);

CREATE USER captain;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE tiltship.signups to captain;
