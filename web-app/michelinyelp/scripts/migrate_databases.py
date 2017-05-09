import sqlite3
from michelinyelp.restaurant.models import City, Restaurant, State, Category, RestaurantByCategory
import re
from localflavor.us import us_states


def run(*args):
    state_map = {'IL': 'Illinois', 'CA': 'California', 'NY': 'New York'}
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    count = 0
    res = ("""SELECT name, rating, url, price, review_count, street, city, state, country, zip_code, phone, image_url FROM restaurant""")  # noqa
    for result in c.execute(res):
        _city, _state = None, None
        try:
            print 'searching for city {}'.format(result[6])
            _city = City.objects.get(name=result[6])
        except City.DoesNotExist:
            print 'ERROR: {} not found in cities'.format(result[6])
        print 'searching for state {}'.format(result[7])
        try:
            _state = State.objects.get(name=state_map[result[7]])
        except State.DoesNotExist:
            print 'ERROR: {} not found in states'.format(result[7])

        if _city and _state:
            r = Restaurant(name=result[0], rating=result[1],
                           url=result[2], price=result[3],
                           review_count=result[4], street=result[5],
                           city=_city, state=_state, zip_code=result[9],
                           phone=result[10], image_url=result[11]
                            )
            count += 1
            print r.name, count
            r.save()

    res = ("""SELECT r.name, c.title FROM restaurant AS r, category AS c, restaurant_by_category AS rbc WHERE r.id = rbc.restaurant_id AND c.id = rbc.category_id""")
    for result in c.execute(res):
        print result
        category = None
        try:
            category = Category.objects.get(title=result[1])
        except Category.DoesNotExist:
            # category = Category.objects.create(title=result[1])
            print 'ERROR: {} not found in categories'.format(result[1])

        restaurant = Restaurant.objects.filter(name=result[0]).first()
        if restaurant and category:
            rbc = RestaurantByCategory(restaurant_id=restaurant,
                                       category_id=category)
            print rbc
            rbc.save()
