from __future__ import unicode_literals
from django.db import models
from localflavor.us.models import (USStateField, USZipCodeField,
                                   PhoneNumberField)


class Address(models.Model):
  street = models.CharField(max_length=100, blank=True, null=True)
  city = models.CharField(max_length=100, null=True, blank=True)
  state_name = USStateField(blank=True, null=True)
  state_abbreviation = models.CharField(max_length=2, blank=True, null=True)
  zip_code = USZipCodeField(blank=True, null=True)

class Restaurant(models.Model):
  name = models.CharField(max_length=100)
  rating = models.DecimalField(max_digits=2, decimal_places=1, null=True,
      blank=True)
  url = models.CharField(max_length=300, blank=True, null=True)
  price = models.CharField(max_length=4)
  review_count = models.IntegerField(blank=True, null=True)
  phone = models.CharField(max_length=14, blank=True, null=True)
  image_url = models.CharField(max_length=300, blank=True, null=True)
  address = models.ForeignKey(Address)

class Review(models.Model):
  url = models.CharField(max_length=300)
  restaurant_id = models.IntegerField(blank=True, null=True)
  rating = models.DecimalField(max_digits=2, decimal_places=1, null=True,
      blank=True)
  name = models.CharField(max_length=100, blank=True, null=True)
  time = models.DateTimeField(blank=True, null=True)
  text = models.CharField(max_length=100, blank=True, null=True)

class Category(models.Model):
  title = models.CharField(max_length=100, blank=True, null=True)

class RestaurantByCategory(models.Model):
  restaurant_id = models.ForeignKey(Restaurant)
  category_id = models.ForeignKey(Category)
