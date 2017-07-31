-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (id SERIAL PRIMARY KEY,
					   name text );

CREATE TABLE matches (match SERIAL PRIMARY KEY,
					  winner int REFERENCES players (id),
					  loser int REFERENCES players (id));

CREATE VIEW wins AS (SELECT players.id, players.name, count(*) as w 
					 FROM players, matches 
					 WHERE players.id = matches.winner 
					 GROUP BY players.id 
					 ORDER BY w desc);

CREATE VIEW losses AS (SELECT players.id, players.name, count(*) as l 
					   FROM players, matches 
					   WHERE players.id = matches.loser 
					   GROUP BY players.id 
					   ORDER BY l desc);

CREATE VIEW total_matches AS (select players.id, players.name, count(*) as matches 
							  from matches, players 
							  where players.id = matches.winner or players.id = matches.loser 
							  group by players.id);

CREATE VIEW standings AS (select players.id, players.name, coalesce(wins.w, wins.w, 0) as wins, 
						  coalesce(total_matches.matches, total_matches.matches, 0) as Matches_played 
						  from players FULL OUTER JOIN wins ON players.id = wins.id 
						  FULL OUTER JOIN  total_matches ON players.id = total_matches.id order by wins desc);
