-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- DROP DATABASE tournament IF EXISTS;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE Players (
	plid SERIAL PRIMARY KEY,
	name VARCHAR(50)
	);

CREATE TABLE Scores (
	plid INTEGER REFERENCES Players,
	score INTEGER
	);

CREATE TABLE Matches (
	plid INTEGER REFERENCES Players
	);
	

