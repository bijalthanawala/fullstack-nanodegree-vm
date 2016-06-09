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
    query = """
            UPDATE Players 
            SET match_count=0
            """
    pgcurs.execute(query)
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
    result = pgcurs.fetchone()
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
    query = "INSERT INTO Players (name) VALUES (%s);"
    pgcurs.execute(query, (name,))
    pgconn.commit()
    print "bj: registerPlayer: Exit"


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
    print "bj: playerStandings: Entry"
    results = []
    pgconn = connect()
    pgcurs = pgconn.cursor()
    query = """
            SELECT plid, name, victories, match_count
            FROM players LEFT JOIN 
                (SELECT plid_win, COUNT(plid_win) AS victories 
                 FROM matches GROUP BY plid_win ORDER BY victories) AS inner_mtach 
            ON plid_win=plid;
            """
    pgcurs.execute(query)
    rows = pgcurs.fetchall()
    print "rows = ", rows
    for row in rows:
        print "row = ", row
        #onetuple = (row['plid'], row['name'], row['victories'], row['match_count'])
        listrow = list(row)
        if not listrow[2]:
            listrow[2] = 0
        row = tuple(listrow)
        print "row = ", row
        results.append(row)
    print "bj: playerStandings: Exit"
    print "results =", results 
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    print "bj: reportMatch: Entry"
    pgconn = connect()
    pgcurs = pgconn.cursor()
    print "type=",type(winner)
    query = "INSERT INTO Matches (plid_win,plid_lose) VALUES (%s,%s);"
    pgcurs.execute(query, (winner,loser))
    pgconn.commit()
    query = """
            UPDATE Players 
            SET match_count=match_count+1
            WHERE plid=%s OR plid=%s;
            """
    pgcurs.execute(query, (winner,loser))
    pgconn.commit()
    print "bj: registerPlayer: Exit"
    print "bj: reportMatch: Exit"
 
 
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
    print "bj: swissPairings: Entry"
    print "bj: swissPairings: Exit"


