from __future__ import unicode_literals

from django.db import models
from localflavor.us.models import (USStateField, USZipCodeField,
                                   PhoneNumberField)


class Address(models.Model):
    street = models.CharField(max_length=127, blank=True, null=True)
    city = models.CharField(max_length=127, null=True, blank=True)
    state = USStateField(blank=True, null=True)
    zip_code = USZipCodeField(blank=True, null=True)


class Restaurant(models.Model):
    name = models.CharField(max_length=127)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True,
                                 blank=True)
    url = models.CharField(max_length=127, blank=True, null=True)
    price = models.CharField(max_length=4)
    review_count = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    image_url = models.CharField(max_length=300, blank=True, null=True)
    address = models.ForeignKey(Address)
