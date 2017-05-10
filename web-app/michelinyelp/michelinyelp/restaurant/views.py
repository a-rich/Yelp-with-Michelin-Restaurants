from django.shortcuts import render
from django.views.generic.edit import FormView
from michelinyelp.restaurant.forms import SearchForm
from django.views.generic import TemplateView, DetailView
from michelinyelp.restaurant.models import Restaurant, City, State, Category, RestaurantByCategory, Review


class SearchView(FormView):
    form_class = SearchForm
    template_name = 'SearchView.html'
    success_url = 'search/'

    def form_valid(self, form):
        query = form.cleaned_data['search_field']
        restaurants = Restaurant.objects.filter(name__icontains=query)
        cities = City.objects.filter(name__icontains=query)
        states = State.objects.filter(name__icontains=query)
        categories = Category.objects.filter(title__icontains=query)
        ctx = {}
        ctx['restaurants'] = restaurants
        ctx['cities'] = cities
        ctx['states'] = states
        ctx['categories'] = categories
        ctx['form'] = self.get_form()
        return self.render_to_response(ctx)


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'

    def get_context_data(self, **kwargs):
      context = super(RestaurantDetailView, self).get_context_data(**kwargs)
      context['reviews'] = Review.objects.filter(restaurant_id=self.object.id)
      self.object.url = ':'.join(['https'] + self.object.url.split('https')[1:])
      return context


class CityListView(DetailView):
    model = City
    template_name = 'city_detail.html'


class StateListView(DetailView):
    model = State
    template_name = 'state_detail.html'


class CategoryListView(DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
      context = super(CategoryListView, self).get_context_data(**kwargs)
      restaurants_by_category = RestaurantByCategory.objects.filter(category_id=self.object)
      restaurant_ids = [r.restaurant_id.id for r in restaurants_by_category]
      context['restaurants'] = Restaurant.objects.filter(id__in=restaurant_ids)
      return context

