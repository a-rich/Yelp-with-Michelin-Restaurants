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
def search(loc):

  """
    Extracts the name and location of every restaurant on the given page and
    returns a dictionary of name keys mapping to location values. 'request' is
    a page to be parsed that has been returned by 'requests.get' and
    'first_page' is boolean that indicates whether or not to return the
    temporary results or call 'iterateResults'.
  """
  def getRestaurants(request, first_page):

    """
      Tries to load another page of results and merges a new dictionary of
      restaurants with 'results'. Exits once an invalid response is returned.
      Returns the complete restarant dictionary.
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
    temp_results = {n: {'address': l.split(',')[0],
                        'city': ' '.join(l.split(',')[1].split()[:-1]),
                        'postal_code': l.split()[-1]}
                      for n, l in zip(names, locations)}

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
  Writes a restaurant dictionary 'results' to a binary file. 'append'
  determines whether or not the restaurant dictionary should be appended to or
  overwrite a potentially preexisting output file named 'file_name'.
"""
def saveResults(results, file_name, append=True):
  try:
    FileNotFoundError
  except NameError:
    FileNotFoundError = IOError

  try:
    if append:
      with open(file_name, 'rb') as f:
        result_list = []
        while True:
          try:
            result_list.append(pickle.load(f))
          except EOFError:
            break

      with open(file_name, 'wb') as f:
        for r in result_list:
          pickle.dump(r, f, protocol=2)
        pickle.dump(results, f, protocol=2)
    else:
      with open(file_name, 'wb') as f:
        pickle.dump(results, f, protocol=2)
  except FileNotFoundError:
    pickle.dump(results, open(file_name, 'wb'), protocol=2)



if __name__ == '__main__':
#############  Demonstration of usage ##############

  output_file = 'michelin_restaurants.bin'

  # These cities have a lot of restaurants -- if you're just testing,
  # it will be a lot faster to run using 'san jose ca' alone
  places_to_search = ['chicago il', 'new york ny', 'san francisco ca']
  #places_to_search = ['san jose ca']

  for place in places_to_search:
    saveResults(search(place), output_file, append=True)

####################################################

  # Prints the results of running the script by reading the output file
  restaurant_locations = []
  f = open(output_file, 'rb')

  while True:
    try:
      restaurant_locations.append(pickle.load(f))
    except EOFError:
      break

  for i, restaurants in enumerate(restaurant_locations):
    print("Restaurants in location", i)
    for name, location in restaurants.items():
      try:
        exec("print '     {:25s} {:s}'.format(name, location)")
      except SyntaxError as e:
        print("     {:25s} {:s}".format(name, str(location)))
