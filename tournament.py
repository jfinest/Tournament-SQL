#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches *;")
    conn.commit() 
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players *;")
    conn.commit() 
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(*) AS total_players_ct FROM players; ")
    ct = c.fetchone()[0]
    return ct
    conn.close()


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    sql = """ INSERT INTO players (name) Values (%s) """
    conn = connect()
    c = conn.cursor()
    c.execute(sql, (name,))
    conn.commit() 
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    sql2 = """ SELECT * from standings; """
    conn = connect()
    c = conn.cursor()
    c.execute(sql2)
    standing = c.fetchall()
    conn.close()
    return standing
    


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    sql = """ INSERT INTO matches (winner,loser) Values (%s,%s) """
    conn = connect()
    c = conn.cursor()
    c.execute(sql, (winner,loser))
    conn.commit() 
    conn.close()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    ranking = playerStandings()
    pairs = []

    i = 0
    remainingPairs = len(ranking) /2

    while remainingPairs > 0:
        pairs.append((ranking[i][0],ranking[i][1],ranking[i+1][0],ranking[i+1][1]))
        i+=2
        remainingPairs -=1

    return pairs










