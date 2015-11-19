-- Table definitions for the tournament project.


-- Use dblink to CREATE DATABASE IF NOT EXISTS,
-- Which is not allowed in PostgreSQL.
-- Workaround copied from:
-- http://stackoverflow.com/questions/18389124/simulate-create-database-if-not-exists-for-postgresql

CREATE EXTENSION IF NOT EXISTS dblink;

SET search_path = blarg,public;

DO
  $do$
    BEGIN
      IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'tournament') THEN
        RAISE NOTICE 'Database already exists';
      ELSE
        PERFORM dblink_exec('dbname=tournament' || current_database(),
                            'CREATE DATABASE tournament');
      END IF;
    END
  $do$

 \c tournament

CREATE TABLE IF NOT EXISTS players (
  player_name text NOT NULL,
  player_id serial PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS matches (
  winner_id INTEGER REFERENCES players(player_id),
  loser_id  INTEGER REFERENCES players(player_id),
  match_id  SERIAL PRIMARY KEY
);


CREATE OR REPLACE VIEW ranking AS
    SELECT winning.player_id,
           winning.player_name,
           winning.wins,
           winning.wins+losing.losses AS number_of_matches,
           ROW_NUMBER() OVER (
             ORDER BY winning.wins DESC,
                      losing.losses ASC
           ) AS rank
    FROM (
        SELECT player_id, player_name, count(winner_id) AS wins
        FROM players LEFT JOIN matches
        ON player_id = winner_id
        GROUP BY player_id
    ) AS winning
    JOIN (
        SELECT player_id, count(loser_id) AS losses
        FROM players LEFT JOIN matches
        ON player_id = loser_id
        GROUP BY player_id
    ) AS losing
    ON winning.player_id = losing.player_id
    ORDER BY winning.wins DESC, losing.losses ASC;
