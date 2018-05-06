#!/usr/bin/env python2

import psycopg2


DATABASE_NAME = "news"

QUESTION1 = "1. What are the most popular three articles of all time?"

QUERY1 = """SELECT articles.title, COUNT(*) AS number
FROM articles, log
WHERE REGEXP_REPLACE(log.path, '/article/', '') = articles.slug
AND log.status = '200 OK'
AND log.path != '/'
GROUP BY articles.title
ORDER BY number DESC
LIMIT 3
"""

QUESTION2 = "2. Who are the most popular articles authors of all time?"

QUERY2 = """SELECT authors.name, COUNT(*) AS number
FROM articles, authors, log
WHERE REGEXP_REPLACE(log.path, '/article/', '') = articles.slug
AND articles.author = authors.id
AND log.status = '200 OK'
AND log.path != '/'
GROUP BY authors.id
ORDER BY number DESC
"""

QUESTION3 = "3. On which days did more than 1% of requests lead to errors?"

QUERY3 = """WITH error_table AS (
SELECT DATE(log.time) AS date, COUNT(*) AS errors
FROM log
WHERE log.status != '200 OK'
GROUP BY date
ORDER BY date), nonerror_table AS (
SELECT DATE(log.time) AS date, COUNT(*) AS nonerrors
FROM log
WHERE log.status = '200 OK'
GROUP BY date
ORDER BY date)
SELECT error_table.date,
ROUND(100.0*CAST(error_table.errors AS NUMERIC)/nonerror_table.nonerrors, 1)
FROM error_table, nonerror_table
WHERE error_table.date = nonerror_table.date
AND 100.0*CAST(error_table.errors AS NUMERIC)/nonerror_table.nonerrors > 1.0
"""

# Date formatting within the SQL query (month name blank-padded to 9 chars)
# QUERY3 = """WITH error_table AS (
# SELECT DATE(log.time) AS date, COUNT(*) AS errors
# FROM log
# WHERE log.status != '200 OK'
# GROUP BY date
# ORDER BY date), nonerror_table AS (
# SELECT DATE(log.time) AS date, COUNT(*) AS nonerrors
# FROM log
# WHERE log.status = '200 OK'
# GROUP BY date
# ORDER BY date)
# SELECT TO_CHAR(error_table.date, 'Month DD, YYYY'),
# ROUND(100.0*CAST(error_table.errors AS NUMERIC)/nonerror_table.nonerrors, 1)
# FROM error_table, nonerror_table
# WHERE error_table.date = nonerror_table.date
# AND 100.0*CAST(error_table.errors AS NUMERIC)/nonerror_table.nonerrors > 1.0
# """


def get_answer(database_name, query):
    """Return output of SQL queries as a list of tuples.

    Keyword arguments:
    dbname: string, database name
    query: string, SQL query

    Return value:
    results: a list of tuples, SQL results
    """
    # Create a new database session, and cursors
    conn = psycopg2.connect(dbname=database_name)
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
    # Format and output answer
    length = len(s)
    for i in range(length):
        print "\"%s\" - %s views" % (s[i][0], s[i][1])
    # Blank line
    print
    # Output second question
    print "%s" % QUESTION2
    # Get SQL query results
    s = get_answer(DATABASE_NAME, QUERY2)
    # Format and output answer
    length = len(s)
    for i in range(length):
        print "%s - %s views" % (s[i][0], s[i][1])
    # Blank line
    print
    # Output third question
    print "%s" % QUESTION3
    # Get SQL query results
    s = get_answer(DATABASE_NAME, QUERY3)
    # Format and output answer
    length = len(s)
    for i in range(length):
        print "%s - %s%% errors" % ('{:%B %d, %Y}'.format(s[i][0]), s[i][1])


if __name__ == "__main__":
    main()
