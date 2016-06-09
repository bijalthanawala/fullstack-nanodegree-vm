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
	name VARCHAR(50),
    match_count INTEGER DEFAULT(0)
	);

-- CREATE TABLE Scores (
-- 	plid INTEGER REFERENCES Players,
--    match_count INTEGER,
--	wins INTEGER
--	);

CREATE TABLE Matches (
    m_id    SERIAL,
	plid_win INTEGER REFERENCES Players(plid),
	plid_lose INTEGER REFERENCES Players(plid)
	);
