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
    print "bj: deleteMatches: Entry"
    pgconn = connect()
    pgcurs = pgconn.cursor()
    sql = "DELETE FROM Matches;"
    pgcurs.execute(sql)
    pgconn.commit()
    pgconn.close()
    print "bj: deleteMatches: Exit"


def deletePlayers():
    """Remove all the player records from the database."""
    print "bj: deletePlayers: Entry"
    pgconn = connect()
    pgcurs = pgconn.cursor()
    sql = "DELETE FROM Players;"
    pgcurs.execute(sql)
    pgconn.commit()
    pgconn.close()
    print "bj: deletePlayers: Exit"


def countPlayers():
    """Returns the number of players currently registered."""
    print "bj: countPlayers: Entry"
    pgconn = connect()
    pgcurs = pgconn.cursor()
    query = "SELECT COUNT(*) FROM Players;"
    pgcurs.execute(query)
    result = pgconn.fetchone()
    count = result[0]
    print "bj: countPlayers: Exit"
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    print "bj: registerPlayer: Entry"
    pgconn = connect()
    pgcurs = pgconn.cursor()
    query = "INSERT INTO Players (name) VALUES ('%s');"
    pgcurs.execute(query, (name,))
    print "bj: registerPlayer: Exit"
    return count


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


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 
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


