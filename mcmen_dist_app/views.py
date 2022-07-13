
from turtle import title
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from mcmen_dist_app.models import PostComment, Property
from mcmen_dist_app.models import Driver
from mcmen_dist_app.models import Route
from mcmen_dist_app.models import Article, PostComment
from mcmen_dist_app.models import Images
from mcmen_inventory_app.models import Brewer

from decouple import config

#--> Rest
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from .serializers import PropertySerializer
from rest_framework.response import Response
#-->

def landing(request):
    return render(request, 'pages/landing.html')

@login_required
def index(request):
    return render(request, 'pages/index.html')

@login_required
def router(request):
    return render(request, 'pages/router.html')

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('router')
    else:
        messages.warning(request, 'User Name or Password is incorrect')
        return render(request, 'pages/landing.html')

def logout_user(request):
    logout(request)
    return redirect('landing')

@login_required
def all_routes(request):
  routes = Route.objects.all()
  props = Property.objects.all()
  return render(request, 'pages/view_routes.html', {'routes': routes, 'props': props})

@login_required
def search_routes(request):
    if request.method == 'GET':
        return render(request, 'pages/search_routes.html') 
    elif request.method == 'POST':
        props = Property.objects.all()
        routes = Route.objects.all()
        # print(routes)
        route_truck = request.POST['truck_num']
        route_day = request.POST['day']
        # print(route_truck, route_day)
        day_route = Route.objects.filter(truck_num=route_truck, day=route_day)
        # print(day_route)
    return render(request, 'pages/search_routes.html', {'day_route': day_route, 'props': props})

@login_required
def add_driver_post(request):
    current_user = request.user
    if request.method == 'GET':
        return render(request, 'pages/add_driver_post.html')
    elif request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        # pub_date = request.POST['pub_date']
        author = (current_user.first_name + ' ' + current_user.last_name)
        Article.objects.create(author = author, title = title, text = text)
        return redirect('view_all_posts')

@login_required
def view_all_posts(request):
  articles = Article.objects.all()
  comments = PostComment.objects.all()
  context = {'articles': articles, 'comments': comments}
#   print(comments)
  return render(request, 'pages/view_posts.html', context)

@login_required
def post_details(request, id):
    article = Article.objects.get(id = id)
    comments = PostComment.objects.filter(post_connected=article.id)
    context = { "article": article, "comments": comments }
    current_user = request.user
    if request.method == 'GET':
        return render(request, 'pages/post_details.html', context)
    elif request.method == 'POST':
        content = request.POST['content']
        author = (current_user.first_name + ' ' + current_user.last_name)
        post_connected = article
        PostComment.objects.create(author = author, post_connected = post_connected, content = content)
        return redirect('view_all_posts')

@login_required
def all_props(request):
  props = Property.objects.all()
  return render(request, 'pages/view_props.html', {'props': props})

@login_required
def prop_details(request, id):
    prop = Property.objects.get(id = id)
    latX= prop.latitude
    lngX= prop.longitude
    key= config("WEATHER_KEY")
    note_list= prop.notes.split("#")
    # print('coordinates ',latX, lngX)
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={latX}&lon={lngX}&units=imperial&appid={key}')
    weather_data = response.json()
    # print(weather_data)
    main= weather_data['main']
    weather= weather_data['weather'][0]
    context= {'prop': prop, 'main': main, 'weather': weather, 'note_list': note_list}
    return render(request, 'pages/prop_details.html', context)

@api_view(['GET'])
def property_detail(request, pk, format=None):
    """
    Retrieve a property by id.
    """
    try:
        property = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PropertySerializer(property)
        return Response(serializer.data)

@login_required
def contacts(request):
  drive_staff = Driver.objects.all()
  brew_staff = Brewer.objects.all()
  context = {'drive_staff': drive_staff, 'brew_staff' :brew_staff}
  return render(request, 'pages/contacts.html', context)

@login_required
def calendar(request):
  return render(request, 'pages/calendar.html')

@login_required
def place_order(request):
  return render(request, 'pages/place_order.html')