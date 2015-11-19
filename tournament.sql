-- Table definitions for the tournament project.


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
