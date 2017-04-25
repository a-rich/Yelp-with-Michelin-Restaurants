import os
import sys
import time
import json

if sys.version_info[0] < 3:
  import cPickle as pickle
else:
  import pickle

"""
    Takes in a function and list of arguments, times the execution of that
    function on those arguments, prints the elapsed time, and returns the
    result of the evaluated function.
"""
def timer(fn, args):
  print("\nExecuting {0}...".format(fn.__name__))
  start = time.time()
  result = fn(args)
  print("Elapsed time: {0}".format(time.time() - start))
  return result

"""
  Takes in a path to a binary file and returns a list of dictionaries that are
  stored in that file.
"""
def getMichelinRestaurants(bin_file):
  restaurant_locations = {}
  f = open(bin_file, 'rb')
  while True:
    try:
      obj = pickle.load(f)
      restaurant_locations[list(obj.keys())[0]] = list(obj.values())[0]
    except EOFError:
      break
  f.close()
  return restaurant_locations

"""
  Takes in a path to a Yelp dataset and a dictionary of restaurants that are,
  themselves, dictionaries of name/location key/value pairs. Each restaurant is
  keyed by the location searched to scrape the restaurants. Returns a
  dictionary of records that are the intersection of restaurants between the
  Yelp dataset and the 'michelin_restaurants' dictionary.
"""
def parseRestaurants(yelp_data, michelin):
  with open('categories_of_interest.txt', 'r') as f:
    categories_of_interest = set(l.strip() for l in f.readlines())
  with open('states_in_yelp_dataset.txt', 'r') as f:
    states_of_interest = set(l.strip() for l in f.readlines())
  with open('cities_in_yelp_dataset.txt', 'r') as f:
    cities_of_interest = set(l.strip() for l in f.readlines())

  restaurant_counts = {}
  with open(yelp_data, 'r') as f:
    data = [json.loads(d) for d in f.readlines()]
  data = list(filter(None, [d if d['state'] in states_of_interest
          and d['city'] in cities_of_interest
          and d['categories'] else None for d in data]))
  for d in data:
    try:
      restaurant_counts[d['state'].lower()][d['city'].lower()] += 1
    except KeyError:
      restaurant_counts[d['state'].lower()] = {city.lower(): 0 for city in
          list(filter(None, [dat['city'].lower() if
        dat['state'].lower() == d['state'].lower() else None for dat in data]))}
  return restaurant_counts
  """
  with open(yelp_data, 'r') as dataset:
    for line in dataset:
      obj = json.loads(line)
      if obj['state'] in states_of_interest and \
          obj['city'] in cities_of_interest and obj['categories']:
        for c in obj['categories']:
          if c in categories_of_interest:
            for _, r in michelin.items():
              if obj['name'] in r:
                print("obj['name']: {0}\nobj['state']: {1}\nobj['city']: {2}\nobj['address']: {3}\n".format(obj['name'], obj['state'], obj['city'], obj['address']))
            break
  """


if __name__ == '__main__':
  start = time.time()
  if os.path.isfile('database.db'):
    print("Already created database.\n \
        Delete 'database.db' to recreate the database.\n \
        Delete 'restaurants.dat' to parse 'restaurants.bin' from scratch.")
  else:
    if os.path.isfile('restaurants.dat'):
      print("Already parsed restaurant data...these will be used to write to the database.")
      restaurants = timer(pickle.load, open('restaurants.dat', 'rb'))
    else:
      print("Parsing restaurants...these will be used to write to the database.")
      restaurants = timer(getMichelinRestaurants, sys.argv[1])

  restaurant_counts = parseRestaurants('yelp_academic_dataset_business.json', restaurants)
