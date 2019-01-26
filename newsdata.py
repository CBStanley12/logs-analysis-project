#!/usr/bin/env python2

"""Analyze mock news data in a PostgreSQL database.

SQL Queries Available:
pop_articles -- returns the top 3 most popular articles (by page views)
pop_authors -- returns the most popular articles (by page views)
req_errors -- returns the days on which more than 1% of requests led to errors
"""

import psycopg2

DBNAME = "news"

pop_articles = """SELECT title, COUNT(log.path) AS num
                FROM articles, log
                WHERE (articles.slug = SUBSTRING(log.path, 10))
                GROUP BY title
                ORDER BY num DESC
                LIMIT 3;"""

pop_authors = """SELECT authors.name, sum(DISTINCT subq.num) AS total
                FROM authors,
                    (SELECT title, author, count(log.path) AS num
                    FROM articles, log
                    WHERE (articles.slug = substring(log.path, 10))
                    GROUP BY title, author
                    ORDER BY num DESC) AS subq
                WHERE authors.id = subq.author
                GROUP BY authors.name
                ORDER BY total DESC;"""

req_errors = """SELECT *
                FROM
                    (SELECT time::DATE,
                        round( 100.0 * ( sum(
                            CASE
                                WHEN status = '404 NOT FOUND' THEN 1
                                ELSE 0
                            END )::DECIMAL / COUNT(status)), 1) AS perc_err
                    FROM log
                    GROUP BY time::DATE
                    ORDER BY perc_err DESC ) AS subq
                WHERE perc_err > 1.0;"""


def log_results(query, mode="w+"):
    """Write the results of an SQL query to a .txt file.

    Arguments:
    query -- the SQL query to be executed
    mode -- the mode used to open the .txt file (default "w+")
    """
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    c.execute(query)
    res = c.fetchall()
    db.close()
    with open("./log_results.txt", mode) as f:
        if (query == pop_articles):
            f.write('\n\nTop 3 Most Popular Articles:')
            for i, (title, views) in enumerate(res, 1):
                f.write('\n{}. "{}" - {} views'.format(i, title, views))
            f.close()
        elif (query == pop_authors):
            f.write("\n\nMost Popular Authors:")
            for i, (author, views) in enumerate(res, 1):
                f.write('\n{}. {} - {} views'.format(i, author, views))
            f.close()
        elif (query == req_errors):
            f.write("\n\nDays Where More Than 1% of Requests Lead to Errors:")
            for date, perc_err in res:
                f.write(u"\n\u2022 {} - {}% errors".format(
                    date.strftime('%B %d, %Y'), perc_err).encode('utf-8'))
            f.close()
        else:
            for desc, value in res:
                f.write(u"\n\u2022 {} - {}".format(desc, value).encode(
                    'utf-8'))
            f.close()


if __name__ == '__main__':
    log_results(pop_articles)
    log_results(pop_authors, "a")
    log_results(req_errors, "a")
