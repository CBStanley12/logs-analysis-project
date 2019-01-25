#!/usr/bin/env python2

import psycopg2

DBNAME = "news"


def pop_articles():
    """Returns the top 3 most popular articles (by page views)"""
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    c.execute("""SELECT title, COUNT(log.path) AS num
            FROM articles, log
            WHERE (articles.slug = SUBSTRING(log.path, 10))
            GROUP BY title
            ORDER BY num DESC
            LIMIT 3;""")
    res = c.fetchall()
    db.close()
    with open("./log_results.txt", "w") as f:
        f.write("\n\nTop 3 Most Popular Articles:")
        for i, (title, views) in enumerate(res, 1):
            f.write('\n{}. "{}" - {} views'.format(i, title, views))
        f.close()


def pop_authors():
    """Returns the most popular authors (by page views)"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT authors.name, sum(DISTINCT subq.num) AS total
            FROM authors,
                (SELECT title, author, count(log.path) AS num
                FROM articles, log
                WHERE (articles.slug = substring(log.path, 10))
                GROUP BY title, author
                ORDER BY num DESC) AS subq
            WHERE authors.id = subq.author
            GROUP BY authors.name
            ORDER BY total DESC;""")
    res = c.fetchall()
    db.close()
    with open("./log_results.txt", "a") as f:
        f.write("\n\nMost Popular Authors: ")
        for i, (name, views) in enumerate(res, 1):
            f.write("\n{}. {} - {} views".format(i, name, views))
        f.close()


def req_errors():
    """Returns the day(s) on which more than 1% of requests lead to errors"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT *
            FROM
                ( SELECT time::DATE,
                    round( 100.0 * ( sum(
                        CASE
                            WHEN status = '404 NOT FOUND' THEN 1
                            ELSE 0
                        END )::DECIMAL / COUNT(status)), 1) AS perc_err
                FROM log
                GROUP BY time::DATE
                ORDER BY perc_err DESC ) AS subq
            WHERE perc_err > 1.0;""")
    res = c.fetchall()
    db.close()
    with open("./log_results.txt", "a") as f:
        f.write("\n\nDays Where More Than 1% of Requests Lead to Errors:")
        for date, perc_err in res:
            f.write(u"\n\u2022 {} - {}% errors".format(date.strftime
                    ('%B %d, %Y'), str(perc_err)).encode('utf-8'))


if __name__ == '__main__':
    pop_articles()
    pop_authors()
    req_errors()
