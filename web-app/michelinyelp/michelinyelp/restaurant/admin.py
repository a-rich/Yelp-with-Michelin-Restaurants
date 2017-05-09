from django.contrib import admin
from michelinyelp.restaurant.models import Restaurant, City, State, Category, Review, RestaurantByCategory


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
  list_display = ['name', 'rating']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
  list_display = ['name']


@admin.register(State)
class RestaurantAdmin(admin.ModelAdmin):
  list_display = ['name', 'abbreviation']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['title']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
  list_display = ['restaurant_id', 'time', 'text', 'url']


@admin.register(RestaurantByCategory)
class RestaurantByCategoryAdmin(admin.ModelAdmin):
  list_display = ['restaurant_id', 'category_id']
