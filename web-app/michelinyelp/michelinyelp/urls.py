"""michelinyelp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from michelinyelp.restaurant.views import (SearchView, RestaurantDetailView,
                                           CityListView, StateListView,
                                           CategoryListView, CategoryAllView,
                                           StateAllView, CityAllView,
                                           RestaurantAllView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', SearchView.as_view()),
    url(r'restaurants/$', RestaurantAllView.as_view(), name='restaurants'),
    url(r'cities/$', CityAllView.as_view(), name='cities'),
    url(r'states/$', StateAllView.as_view(), name='states'),
    url(r'categories/$', CategoryAllView.as_view(), name='categories'),
    url(r'restaurants/(?P<pk>[-\w]+)/$', RestaurantDetailView.as_view(), name='restaurant'),
    url(r'cities/(?P<pk>[-\w]+)/$', CityListView.as_view(), name='city'),
    url(r'states/(?P<pk>[-\w]+)/$', StateListView.as_view(), name='state'),
    url(r'categories/(?P<pk>[-\w]+)/$', CategoryListView.as_view(), name='category'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
