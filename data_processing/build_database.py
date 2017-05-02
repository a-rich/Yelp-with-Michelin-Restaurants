import sys
import sqlite3
from sqlite3 import Error
import pickle

michelin = pickle.load(open('michelin_restaurants.bin', 'rb'))
yelp_restaurants = pickle.load(open('yelp_restaurants.bin', 'rb'))
yelp_reviews = pickle.load(open('yelp_reviews.bin', 'rb'))

create_table_sql = """PRAGMA foreign_keys = ON;

                      CREATE TABLE IF NOT EXISTS state (
                        id INT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL
                      );

                      CREATE TABLE IF NOT EXISTS city (
                        id INT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL
                      );

                      CREATE TABLE IF NOT EXISTS restaurant (
                        id INT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        rating FLOAT,
                        url VARCHAR(300),
                        price VARCHAR(4),
                        review_count INT,
                        street VARCHAR(100),
                        city VARCHAR(100),
                        state VARCHAR(2),
                        country VARCHAR(100),
                        zip_code INT,
                        phone VARCHAR(20),
                        image_url VARCHAR(300)
                      );

                      CREATE TABLE IF NOT EXISTS category (
                        id INT PRIMARY KEY,
                        title VARCHAR(100)
                      );

                      CREATE TABLE IF NOT EXISTS restaurant_by_category (
                        restaurant_id INT,
                        category_id INT,
                        FOREIGN KEY (restaurant_id) REFERENCES restaurant,
                        FOREIGN KEY (category_id) REFERENCES category
                      );

                      CREATE TABLE IF NOT EXISTS review (
                        url VARCHAR(300) PRIMARY KEY,
                        restaurant_id INT,
                        rating FLOAT,
                        name VARCHAR(100),
                        time VARCHAR(100),
                        text VARCHAR(300)
                      );
                   """

try:
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.executescript(create_table_sql)
  c.close()
  conn.close()
except Error as e:
  print(e)

state_id = city_id = restaurant_id = category_id = 0
seen_states, seen_cities, seen_categories = set(), set(), set()
sql = ""
for place in michelin.keys():
  print("Building SQL string for {0} restaurants...".format(place))
  for r in yelp_restaurants[place]:
    if r['name'] in michelin[place].keys():
      sql += """INSERT INTO restaurant VALUES({0}, "{1}", {2}, "{3}", "{4}", {5}, "{6}", "{7}", "{8}", "{9}", {10}, "{11}", "{12}");\n""".format(
          restaurant_id,
          r['name'].replace('\"', '\'').replace(':', ''),
          r['rating'],
          r['url'].replace('\"', '\'').replace(':', ''),
          r['price'].replace('\"', '\'').replace(':', ''),
          r['review_count'],
          r['location']['address1'].replace('\"', '\'').replace(':', ''),
          r['location']['city'].replace('\"', '\'').replace(':', ''),
          r['location']['state'].replace('\"', '\'').replace(':', ''),
          r['location']['country'].replace('\"', '\'').replace(':', ''),
          r['location']['zip_code'].replace('\"', '\'').replace(':', ''),
          r['display_phone'],
          r['image_url'],
      )

      if r['location']['city'] not in seen_cities:
        sql += """INSERT INTO city VALUES({0}, "{1}");\n""".format(
            city_id,
            r['location']['city'].replace('\"', '\'').replace(':', '')
            )
        seen_cities.add(r['location']['city'])
        city_id += 1

      if r['location']['state'] not in seen_states:
        sql += """INSERT INTO state VALUES({0}, "{1}");\n""".format(
            state_id,
            r['location']['state'].replace('\"', '\'').replace(':', '')
            )
        seen_states.add(r['location']['state'])
        state_id += 1

      for category in set([c['title'] for c in r['categories']]):
        if category not in seen_categories:
          sql += """INSERT INTO category VALUES({0}, "{1}");\n""".format(
              category_id,
              category.replace('\"', '\'').replace(':', '').replace('(', '')
              )
          seen_categories.add(category)
          category_id += 1

        sql += """INSERT INTO restaurant_by_category VALUES({0}, {1});\n""".format(
            restaurant_id,
            list(sorted(seen_categories)).index(category)
            )

      for review in yelp_reviews[place][r['id']]['reviews']:
        sql += """INSERT INTO review VALUES("{0}", {1}, {2}, "{3}", "{4}", "{5}");\n""".format(
            review['url'].replace('\"', '\''),
            restaurant_id,
            review['rating'],
            review['user']['name'].replace('\"', '\'').replace(':', ''),
            review['time_created'].replace('\"', '\'').replace(':', ''),
            review['text'].replace('\"', '\'').replace(':', '')
            )
      restaurant_id += 1
try:
  print("Adding records to the database...")
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.executescript(sql)
  conn.commit()
  conn.close()
except Error as e:
  print(e)
