import os
import pickle
from yelpapi import YelpAPI

client_id = "TgDi75JA_PwGLZfvhAmGyw"
client_secret = "W3cSrl16Dp6vkLlqnghQo2cYbzlX173rnNyRVydNIrd16MroG8c5xTMrDJ5J3GLb"
api = YelpAPI(client_id, client_secret)

def findRestaurants():
  locations = {'chicago il': [],
               'new york ny': [],
               'san francisco ca': []
               }

  for loc in locations.keys():
    offset = 0
    while True:
      try:
        locations[loc] += api.search_query(term='restaurant', location=loc,
            limit=50, offset=offset)['businesses']
        offset += 50
      except YelpAPI.YelpAPIError:
        break

  pickle.dump(locations, open('yelp_restaurants.bin', 'wb'), protocol=2)
  return locations

def findReviews(locations):
  reviews = {'chicago il': {},
             'new york ny': {},
             'san francisco ca': {}
             }

  for place in locations:
    print("\nFetching reviews in {0}\n".format(place))
    for restaurant in [r for r in locations[place]]:
      print("Getting reviews for", restaurant['id'])
      try:
        reviews[place][restaurant['id']] = api.reviews_query(id=restaurant['id'])
      except YelpAPI.YelpAPIError:
        break

  pickle.dump(reviews, open('yelp_reviews.bin', 'wb'), protocol=2)
  return reviews


if __name__ == '__main__':
  if os.path.isfile('yelp_restaurants.bin'):
    print("Yelp restaurant data structure has already been computed. Loading from file...")
    locations = pickle.load(open('yelp_restaurants.bin', 'rb'))
  else:
    locations = findRestaurants()

  if os.path.isfile('yelp_reviews.bin'):
    print("Yelp review data structure has already been computed. Loading from file...")
    reviews = pickle.load(open('yelp_reviews.bin', 'rb'))
  else:
    reviews = findReviews(locations)
