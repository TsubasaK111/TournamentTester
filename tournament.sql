-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

CREATE TABLE matches (
  winner_id INTEGER REFERENCES players(player_id),
  losing_id INTEGER REFERENCES players(player_id),
  match_id      serial PRIMARY KEY
);

CREATE TABLE players (
  player_name text,
  player_id serial PRIMARY KEY
);
