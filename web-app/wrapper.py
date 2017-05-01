import sqlite3
import time
from sqlite3 import Error

class MichelinStarredAPI:
  __conn = None

  """
    Connects to the database named in the parameter, fetches the maximum ID in
    order to set __next_pub_id, and turns on foreign key contraints.
  """
  def __init__(self, database):
    try:
      self.__conn = sqlite3.connect(database)
      cursor = self.__conn.cursor()
      cursor.execute("""PRAGMA foreign_keys = ON""").close()
    except Error as e:
      print(e)

  """
  """
  def queryPublication(self, record, exact=True, output_format='JSON',
      sorted_order='title', reverse=False, queryRange="0,50"):
    author, title, year, journal = record[0], record[1], record[2], record[3]
    start, end = queryRange.split(',')[0], queryRange.split(',')[1]

    cond1 = '' if not author else "lower(a.name) = '{0}'".format(author.lower())
    cond2 = '' if not title else "lower(p.title) = '{0}'".format(title.lower())
    cond3 = '' if not year else "p.year = {0}".format(year)

    cond1 = cond1 + " AND " if cond1 and (cond2 or cond3 or cond4) else cond1
    cond2 = cond2 + " AND " if cond2 and (cond3 or cond4 ) else cond2
    cond3 = cond3 + " AND " if cond3 and cond4 else cond3
    cond5 = "AND " if cond1 or cond2 or cond3 or cond4 else ""
    cond6 = "ORDER BY " + sorted_order + " DESC" if reverse else "ORDER BY " + sorted_order

    sql_pubs = """SELECT DISTINCT p.id, p.title, p.year, p.booktitle
                  FROM publication as p, written_by as w, author as a
                  WHERE p.id = w.pub_id and w.author_id = a.id
                  {4} {0}{1}{2}{3} {5} LIMIT {6},{7};
              """.format(cond1, cond2, cond3, cond4, cond5, cond6, start, end)

    sql_authors = """SELECT p.id, a.name
                     FROM publication as p, written_by as w, author as a
                     WHERE p.id = w.pub_id and w.author_id = a.id
                     {4} {0}{1}{2}{3} {5};
                  """.format(cond1, cond2, cond3, cond4, cond5, cond6)

    try:
      cursor = self.__conn.cursor()
      result_pubs = cursor.execute(sql_pubs).fetchall()
      result_authors = cursor.execute(sql_authors).fetchall()
      cursor.close()
    except Error as e:
      print(e)

if __name__ == '__main__':
  api = MichelinStarredAPI('../data_processing/database.db')
