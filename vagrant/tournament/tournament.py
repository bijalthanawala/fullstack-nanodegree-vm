#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def db_open():
    """Returns a database connection, and cursor"""
    pgconn = connect()
    pgcurs = pgconn.cursor()
    return (pgconn, pgcurs)


def db_close(pgconn, do_commit=True):
    """Closes a database connection, after commiting(if requested to)"""
    if do_commit:
        pgconn.commit()
    pgconn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    (pgconn, pgcurs) = db_open()
    sql = "DELETE FROM Matches;"
    pgcurs.execute(sql)
    db_close(pgconn)


def deletePlayers():
    """Remove all the player records from the database."""
    (pgconn, pgcurs) = db_open()
    sql = "DELETE FROM Players;"
    pgcurs.execute(sql)
    db_close(pgconn)


def countPlayers():
    """Returns the number of players currently registered."""
    (pgconn, pgcurs) = db_open()
    query = "SELECT COUNT(*) FROM Players;"
    pgcurs.execute(query)
    result = pgcurs.fetchone()
    count = result[0]
    db_close(pgconn, False)
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    (pgconn, pgcurs) = db_open()
    query = "INSERT INTO Players (name) VALUES (%s);"
    pgcurs.execute(query, (name,))
    db_close(pgconn)


def getNumberOfMatches(playerid):
    """
    Returns number of matches playes by a player
    """

    (pgconn, pgcurs) = db_open()
    query = """
            SELECT COUNT(*) FROM Matches
            WHERE pl_id_win = %s OR pl_id_lose = %s
            """
    pgcurs.execute(query, (playerid, playerid))
    row = pgcurs.fetchone()
    match_count = row[0]
    db_close(pgconn)
    return match_count


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    plStandings = []
    (pgconn, pgcurs) = db_open()
    query = """
            SELECT  pl_id,
                    name,
                    CASE WHEN victories IS NOT NULL
                       THEN victories
                       ELSE 0 END AS victories
            FROM Players LEFT JOIN
                (SELECT pl_id_win, COUNT(pl_id_win) AS victories
                 FROM Matches
                 GROUP BY pl_id_win)
                AS inner_match
            ON pl_id_win=pl_id
            ORDER BY victories;
            """
    pgcurs.execute(query)
    rows = pgcurs.fetchall()
    for row in rows:
        plrecord = list(row)
        no_of_matches = getNumberOfMatches(plrecord[0])
        plrecord.append(no_of_matches)
        row = tuple(plrecord)
        plStandings.append(row)
    db_close(pgconn, False)
    return plStandings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    (pgconn, pgcurs) = db_open()
    query = "INSERT INTO Matches (pl_id_win, pl_id_lose) VALUES (%s,%s);"
    pgcurs.execute(query, (winner, loser))
    db_close(pgconn)


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
    swisspairs = []
    results = playerStandings()
    nr_pairs = len(results) / 2
    for i in range(nr_pairs):
        off = i*2
        apair = (results[off][0], results[off][1],
                 results[off+1][0], results[off+1][1])
        swisspairs.append(apair)
    return swisspairs
