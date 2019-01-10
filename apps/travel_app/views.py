from django.shortcuts import render,redirect
from django.contrib import messages
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from .models import *

import bcrypt



def index(request):
    return render(request,"index.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    
    if len(errors):
        for errors, error in errors.items():
            messages.error(request, error)
        return redirect('/')
    
    hashed =  bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    decoded_hash = hashed.decode('utf-8')
    user = User.objects.create(first_name = request.POST['first_name'], last_name= request.POST['last_name'], email= request.POST['email'], password = decoded_hash)
    # Now store that user id in session as their ticket to move through the application
    request.session['user_id'] = user.id
    
    return redirect('/dashboard')


def login(request):
    user_list = User.objects.filter(email = request.POST['email'])
    if not user_list:
            messages.error(request, 'Invalid Credentials')
            return redirect('/')
    user = user_list[0]
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        print('You are logged in!')
        return redirect('/dashboard')
    else:
        messages.error(request, "Invalid Credentials")
        return redirect('/')

    return redirect('/')

def dashboard(request):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        "other_trips": Trip.objects.exclude(travelers = user),
        "users": User.objects.all(),
        "user": User.objects.get(id = request.session['user_id']),
        "voyages": Trip.objects.all()
  
    }
    return render (request,'dashboard.html', context)

def trip_add(request):
    return render(request, 'add_trip.html')

def add_trip(request):
   
    error = False
    
    if len(request.POST['city']) < 2:
        messages.error(request,'City must contain at least two characters')
        error = True
    elif not request.POST['city'].isalpha():
        messages.error(request,'City cannot contain any numbers')
        error = True
    if len(request.POST['country']) < 2:
        messages.error(request,'Country must contain at least two characters')
        error = True
    elif not request.POST['country'].isalpha():
        messages.error(request,'Country cannot contain any numbers')
        error = True
    if len(request.POST['desc']) < 5:
        messages.error(request,'Please provide a description for this trip')
        error = True
    if len(request.POST['depart'])< 2: 
        messages.error(request,'Please select a depart date')
        error = True
    #Depart cannot be in the past 
    if len(request.POST['return']) < 2:
        messages.error(request,'Please select an return date')
        error = True
    if error:
        messages.error(request,'Try again!')
        return redirect('/trip_add')
    
    user = User.objects.get(id = request.session['user_id'])
    
    user.trips.add(Trip.objects.create(city = request.POST['city'], country = request.POST['country'], description= request.POST['desc'], start_date = request.POST['depart'], end_date = request.POST['return']))

    print('You have successfully added a trip')
    return redirect('/dashboard')
# *****************************************************************************
def join(request,id):
    user = User.objects.get(id = request.session['user_id'])
   # I need to get the id of THAT specific trip ????
    user.trips.add(Trip.objects.get(id = id))
    return redirect('/dashboard')
    
def delete(request,id):
    user = User.objects.get(id = request.session['user_id'])
    # I need to get the id of THAT specific trip ????
    Trip.objects.get(id = id)
    return redirect ('/dashboard')

def cancel(request,id):
    user = User.objects.get(id = request.session['user_id'])
    # I need to get the id of THAT specific trip ????
    user.trips.remove(Trip.objects.get(id=id))
    return redirect ('/dashboard')

# ****************************************************************************