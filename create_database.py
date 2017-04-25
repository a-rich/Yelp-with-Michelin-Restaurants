import os
import sys
import time

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
def parseRestaurants(yelp_data, michelin_restaurants):
  pass


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

  for k, v in restaurants.items():
    print('\n\nMichelin restaurants near {0}:'.format(k))
    for n, l in v.items():
      print("     {:40s} {:s}".format(n, l))

