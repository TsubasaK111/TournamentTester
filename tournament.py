#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament


import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    connection = psycopg2.connect("dbname=tournament")
    cursor = connection.cursor()
    return connection, cursor

def deleteMatches():
    """Remove all the match records from the database."""

    connection, cursor = connect()

    cursor.execute("DELETE FROM matches;")

    connection.commit()
    cursor.close()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""

    connection, cursor = connect()

    cursor.execute("DELETE FROM players;")

    connection.commit()
    cursor.close()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""

    connection, cursor = connect()

    cursor.execute("SELECT count(*) FROM players;")
    return cursor.fetchone()[0]

    cursor.close()
    connection.close()


def registerPlayer(name):
    """
    Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    connection, cursor = connect()

    cursor.execute("INSERT INTO players(player_name) VALUES(%s)", (name,))

    connection.commit()
    cursor.close()
    connection.close()


def playerStandings():
    """
    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played

    Example:
    [(2, "Blue Jays"", 3, 3),(2, "Cardinals", 0, 3)]
    """

    connection, cursor = connect()

    cursor.execute("""
        SELECT
            player_id,
            player_name,
            wins,
            number_of_matches
        FROM
            ranking
        LIMIT 1000;
    """)

    standings = cursor.fetchall()

    cursor.close()
    connection.close()
    return standings


def reportMatch(winner, loser):
    """
    Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    connection, cursor = connect()

    cursor.execute("""
        INSERT INTO matches(winner_id, loser_id)
        VALUES(%s, %s)
    """, (winner, loser, ))

    connection.commit()
    cursor.close()
    connection.close()


def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player
    adjacent to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    connection, cursor = connect()

    cursor.execute("""
        SELECT
            left_player.player_id,
            left_player.player_name,
            right_player.player_id,
            right_player.player_name
        FROM
            (SELECT player_id, player_name, rank
            FROM ranking
            ) AS left_player,
            (SELECT player_id, player_name, rank
            FROM ranking
            ) AS right_player
        WHERE
            left_player.rank+1=right_player.rank
            AND MOD(left_player.rank, 2) = 1
        ORDER BY left_player.rank DESC
        LIMIT 1000;
    """)

    next_pairings = cursor.fetchall()

    cursor.close()
    connection.close()
    return next_pairings
