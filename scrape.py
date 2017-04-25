import sys
import pickle
import requests
from lxml import html

if sys.version_info[0] < 3:
  from urllib import urlencode
else:
  from urllib.parse import urlencode

"""
  Returns a dictionary of Michelin starred restaurants at a given location. The
  parameter 'loc' is a string representing the location you want to search at.
"""
def searchLocation(loc):

  """
    Extracts the name and location of every restaurant on the given page and
    returns a dictionary of name keys mapping to location values.
  """
  def getRestaurants(request, first_page):

    """
      Tries to load another page of results and merges a new dictionary of
      restaurants with the parameter 'restaurants'. Exits once an invalid response
      is returned. Returns the complete restarant dictionary.
    """
    def iterateResults():
      results_page = 2
      while True:
        params = {'address': loc, 'page': results_page}
        request = requests.get(base_url + urlencode(params))
        if request.status_code == 200:
          next_rest = getRestaurants(request, first_page)
          results.update(next_rest)
          results_page += 1
        else:
          break
      return results

    tree = html.fromstring(request.content)
    names = tree.xpath('//div[@class="poi-item-name truncate"]/a/text()')
    locations = tree.xpath('//div[@class="poi-item-address truncate"]/@title')
    if sys.version_info[0] < 3:
      names = [str(n.encode('UTF-8')) for n in names]
      locations = [str(l.encode('UTF-8')) for l in locations]
    temp_results = {n: l for n, l in zip(names, locations)}

    if first_page:
      first_page = False
      results = temp_results
      return iterateResults()
    return temp_results

  params = {'address': loc}
  base_url = 'https://www.viamichelin.com/web/restaurants?'
  request = requests.get(base_url + urlencode(params))
  first_page = True
  return getRestaurants(request, first_page)


"""
  Appends a restaurant dictionary to a binary file. The file may either not
  exist, in which case 'saveResults' will create it, or already exists, in
  which case 'saveResults' will append the parameter 'results' to the file of
  other restaurant dictionary objects.
"""
def saveResults(location, results, file_name):
  try:
    FileNotFoundError
  except NameError:
    FileNotFoundError = IOError

  try:
    f = open(file_name, 'rb')
    result_list = []
    while True:
      try:
        result_list.append(pickle.load(f))
      except EOFError:
        break
    f.close()
    f = open(file_name, 'wb')
    for r in result_list:
      pickle.dump(r, f, protocol=2)
    pickle.dump({location: results}, f, protocol=2)
    f.close()
  except FileNotFoundError:
    pickle.dump({location: results}, open(file_name, 'wb'), protocol=2)



if __name__ == '__main__':
#############  Demonstration of usage ##############
  # Try to be explicit -- may have to try string in browser to ensure matching
  san_jose = 'San Jose California'
  san_francisco = 'San Francisco California'

  SJ_restaurants = searchLocation(san_jose)
  SF_restaurants = searchLocation(san_francisco)

  # Each time you run this, it will append to 'restaurants.bin'
  saveResults(san_jose, SJ_restaurants, 'restaurants.bin')
  saveResults(san_francisco, SF_restaurants, 'restaurants.bin')

  restaurant_locations = []
  f = open('restaurants.bin', 'rb')
  while True:
    try:
      restaurant_locations.append(pickle.load(f))
    except EOFError:
      break

  for restaurants in restaurant_locations:
    try:
      exec("print '\n\nMichelin restaurants near {0}:'".format(list(restaurants.keys())[0]))
    except SyntaxError as e:
      print('\n\nMichelin restaurants near {0}:'.format(list(restaurants.keys())[0]))

    for name, location in list(restaurants.values())[0].items():
      try:
        exec("print '     {:40s} {:s}'.format(name, location)")
      except SyntaxError as e:
        print("     {:40s} {:s}".format(name, location))
####################################################
