#!/usr/bin/env python2

import psycopg2


DATABASE_NAME = "news"

QUESTION1 = "1. What are the most popular three articles of all time?"

QUERY1 = """SELECT title, COUNT(*) AS views
FROM log JOIN articles
ON log.path = CONCAT('/article/', articles.slug)
GROUP BY title
ORDER BY views DESC
LIMIT 3
"""

QUESTION2 = "2. Who are the most popular article authors of all time?"

QUERY2 = """SELECT name, COUNT(*) AS views
FROM authors JOIN articles
ON authors.id = articles.author JOIN log
ON log.path = CONCAT('/article/', articles.slug)
GROUP BY name
ORDER BY views DESC
"""

QUESTION3 = "3. On which days did more than 1% of requests lead to errors?"

QUERY3 = """SELECT TO_CHAR(date, 'FMMonth FMDD, YYYY'),
ROUND(100.0*CAST(err/total AS NUMERIC), 1) AS ratio
FROM (SELECT time::date AS date,
COUNT(*) AS total,
SUM((status != '200 OK')::int)::float as err
FROM log
GROUP BY date) AS errors
WHERE err/total > 0.01;
"""


def get_answer(database_name, query):
    """Return output of SQL queries as a list of tuples.

    Keyword arguments:
    dbname: string, database name
    query: string, SQL query

    Return value:
    results: a list of tuples, SQL results
    """
    try:
        # Create a new database session
        conn = psycopg2.connect(dbname=database_name)
    except psycopg2.DatabaseError as e:
        print "ERROR: cannot connect to the database"
    else:
        # Create a new cursor
        cur = conn.cursor()
        # Execute SQL command
        cur.execute(query)
        # Fetch all rows of a query result
        results = cur.fetchall()
        # Close the cursor object and database session
        cur.close()
        conn.close()
        # Return query results
        return results


def main():
    """Output questions and answers."""
    # Output first question
    print "%s" % QUESTION1
    # Get SQL query results
    s = get_answer(DATABASE_NAME, QUERY1)
    if s is not None:
        # Format and output answer
        for (title, count) in s:
            print "    {} - {} views".format(title, count)
    # Blank line
    print
    # Output second question
    print "%s" % QUESTION2
    # Get SQL query results
    s = get_answer(DATABASE_NAME, QUERY2)
    if s is not None:
        # Format and output answer
        for (author, count) in s:
            print "    {} - {} views".format(author, count)
    # Blank line
    print
    # Output third question
    print "%s" % QUESTION3
    # Get SQL query results
    s = get_answer(DATABASE_NAME, QUERY3)
    if s is not None:
        # Format and output answer
        for (date, rate) in s:
            print "    {} - {}% errors".format(date, rate)


if __name__ == "__main__":
    main()
