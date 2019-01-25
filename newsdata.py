#!/usr/bin/env python2
# !/usr/bin/python2

import psycopg2

DBNAME = "news"


def pop_articles():
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    c.execute("""select title, count(log.path) as num from articles,
            log where (articles.slug = substring(log.path, 10))
            group by title order by num desc limit 3;""")
    res = c.fetchall()
    db.close()
    with open("./log_results.txt", "a") as f:
        f.write("\n\nTop 3 Most Popular Articles:")
        i = 0
        while i < len(res):
            f.write('\n{}. "{}" - {} views'.format((i+1),
                    res[i][0], res[i][1]))
            i += 1
        f.close()


def pop_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select authors.name, sum(subq.num) as total from authors,
            articles, (select title, author, count(log.path) as num from
            articles, log where (articles.slug = substring(log.path, 10))
            group by title, author order by num desc) as subq where authors.id
            = articles.author group by authors.name order by total desc;""")
    res = c.fetchall()
    db.close()
    with open("./log_results.txt", "a") as f:
        f.write("\n\nMost Popular Authors: ")
        i = 0
        while i < len(res):
            f.write("\n{}. {} - {} views".format((i+1), res[i][0], res[i][1]))
            i += 1
        f.close()


def req_errors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select time::date, round( 100.0 * (
            sum(case when status = '404 NOT FOUND' then 1 else 0 end)::decimal
            / count(status)), 1 ) as perc_err from log group by time::date
            order by perc_err desc;""")
    res = c.fetchall()
    db.close()
    with open("./log_results.txt", "a") as f:
        f.write("\n\nDays Where More Than 1% of Requests Lead to Errors:")
        i = 0
        while i < len(res):
            if res[i][1] > 1.0:
                f.write(u"\n\u2022 {} - {}% errors".format(res[i][0].strftime
                        ('%B %d, %Y'), str(res[i][1])).encode('utf-8'))
                i += 1
            else:
                i += 1
        f.close()


if __name__ == '__main__':
    pop_articles()
    pop_authors()
    req_errors()
