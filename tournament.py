#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament


import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM matches;")

    connection.commit()
    cursor.close()
    connection.close()

def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM players;")

    connection.commit()
    cursor.close()
    connection.close()

def countPlayers():
    """Returns the number of players currently registered."""
    connection= connect()
    cursor = connection.cursor()

    cursor.execute("SELECT count(*) FROM players;")
    return cursor.fetchone()[0]

    cursor.close()
    connection.close()

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO players(player_name) VALUES(%s)", (name,))

    connection.commit()
    cursor.close()
    connection.close()

def playerStandings():
    """
    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    Example:
    [(2, "blue jays"", 3, 3),(2, "cardinals", 0, 3)]
    """
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT winning.player_id, winning.player_name, losing.losses, winning.wins
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
        ON winning.player_id = losing.player_id;
    """)

    standings = cursor.fetchall()
    return standings

    cursor.close()
    connection.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO matches(winner_id, loser_id), VALUES(%s, %s)", (winner,loser,))

    connection.commit()
    cursor.close()
    connection.close()

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
