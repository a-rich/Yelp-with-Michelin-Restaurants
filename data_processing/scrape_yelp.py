import pickle
from yelpapi import YelpAPI

client_id = "TgDi75JA_PwGLZfvhAmGyw"
client_secret = "W3cSrl16Dp6vkLlqnghQo2cYbzlX173rnNyRVydNIrd16MroG8c5xTMrDJ5J3GLb"
api = YelpAPI(client_id, client_secret)

locations = {'chicago, il': [],
             'new york, ny': [],
             'san francisco, ca': []}

for loc in locations.keys():
  offset = 0
  while True:
    try:
      locations[loc] += api.search_query(term='restaurant', location=loc,
          limit=50, offset=offset)['businesses']
      offset += 50
    except YelpAPI.YelpAPIError:
      break

pickle.dump(locations, open('yelp_restaurants.bin', 'wb'))
