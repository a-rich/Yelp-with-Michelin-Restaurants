import sqlite3
import time
from sqlite3 import Error

class MichelinStarredAPI:
  __conn = None
  suggestions = None

  """
    Connects to the database named in the parameter, fetches the maximum ID in
    order to set __next_pub_id, and turns on foreign key contraints.
  """
  def __init__(self, database):
    try:
      self.__conn = sqlite3.connect(database)
      cursor = self.__conn.cursor()
      sql = """
              SELECT name, 'city' FROM city
              UNION SELECT name, 'state' FROM state
              UNION SELECT name, 'restaurant' FROM restaurant
              UNION SELECT title, 'category' FROM category;
            """
      self.suggestions = {r[0]: r[1] for r in cursor.execute(sql).fetchall()}
      cursor.close()
    except Error as e:
      print(e)

  def getByCity(self, c):
    try:
      cursor = self.__conn.cursor()
      sql = """
              SELECT name FROM restaurant
              WHERE city = '{0}'
              ORDER BY name;
            """.format(c)
      results = [r[0] for r in cursor.execute(sql).fetchall()]
      cursor.close()
      return results
    except Error as e:
      print(e)

  def getByState(self, s):
    try:
      cursor = self.__conn.cursor()
      sql = """
              SELECT name, city FROM restaurant
              WHERE state = '{0}'
              ORDER BY city, name;
            """.format(s)
      results = [' '.join([r[0]+',', r[1]]) for r in cursor.execute(sql).fetchall()]
      cursor.close()
      return results
    except Error as e:
      print(e)

  def getByCategory(self, c):
    try:
      cursor = self.__conn.cursor()
      sql = """
              SELECT name, city, state FROM restaurant
              WHERE id IN (
                SELECT restaurant_id FROM restaurant_by_category, category
                WHERE category_id = id and title = '{0}'
              )
              ORDER BY state, city, name;
            """.format(c)
      results = [' '.join([r[0]+',', r[1]+',', r[2]]) for r in cursor.execute(sql).fetchall()]
      cursor.close()
      return results
    except Error as e:
      print(e)

  def getByRestaurant(self, r):
    try:
      cursor = self.__conn.cursor()
      sql = """
              SELECT * FROM restaurant
              WHERE name = "{0}";
            """.format(r)
      restaurant = cursor.execute(sql).fetchall()[0]
      sql = """
              SELECT * FROM review
              WHERE restaurant_id = {0};
            """.format(restaurant[0])
      reviews = cursor.execute(sql).fetchall()
      result = (restaurant, reviews)
      cursor.close()
      return result
    except Error as e:
      print(e)

  def triggerQuery(self, word):
    if self.suggestions[word] == 'city':
      return getByCity(word)
    elif self.suggestions[word] == 'state':
      return getByState(word)
    elif self.suggestions[word] == 'category':
      return getByCategory(word)
    else:
      return getByRestaurant(word)

if __name__ == '__main__':
  api = MichelinStarredAPI('../data_processing/database.db')

