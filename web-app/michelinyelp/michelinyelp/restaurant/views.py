from django.shortcuts import render
from django.views.generic.edit import FormView
from michelinyelp.restaurant.forms import SearchForm
from django.views.generic import TemplateView, DetailView
from michelinyelp.restaurant.models import Restaurant, City, State, Category


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


class CityListView(DetailView):
    model = City
    template_name = 'city_detail.html'


class StateListView(DetailView):
    model = State
    template_name = 'state_detail.html'


class CategoryListView(DetailView):
    model = Category
    template_name = 'category_detail.html'
