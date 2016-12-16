from django.shortcuts import render, redirect
from django.db.models import Count
from .models import *

def index(request):
  if 'loggedin' in request.session:
    return redirect("/dashboard")
  else:
    return render(request, "djangobelt/index.html")
  
def login(request):
  if request.POST:
    loggedin = User.objects.login(request, request.POST["email"], request.POST["password"])
  return redirect(index)

def logout(request):
  User.objects.logout(request)
  return redirect(index)

def register(request):
  if not request.POST:
    return redirect(index)
  success = User.objects.register(request, request.POST)
  if not success:
    formdata = request.POST.copy()
    formdata.pop("password")
    formdata.pop("password2")
    request.session["formdata"] = formdata
    return redirect(index)
  return redirect("/dashboard")

def dashboard(request):
  return render(request, "djangobelt/dashboard.html")


def friends(request):
  if 'loggedin' not in request.session:
    errors = ["You must register/log in to access the site!"]
    return render(request, 'djangobelt/index.html', context={'hacks': errors})

  id = request.session['userid']
  
  user = User.objects.get(id=id)

  # Get all users except the logged in user id
  otherusers = User.objects.exclude(id=id)

  # Gets all friend objects where user was beFriended
  myfriends = Friend.objects.filter(befriender = user)

  print "*"*50
  print "user = ",user.id
  print "myfriends = " , myfriends
  print "*"*50
  
  friendlist = []
  for friend in myfriends:
    f = User.objects.get(id=friend.frienduser.id)
    friendlist.append(f)

  context = {
    "friends": friendlist,
    "nonfriends": otherusers
  }
  return render(request, 'djangobelt/dashboard.html', context)

def befrienduser(request, id):
  friends = Friend.objects.filter(frienduser = id).count()
  if friends < 1:
    Friend.objects.friend(request.session['userid'], id)
  return redirect('/dashboard')

def viewuser(request, id):
  if 'loggedin' not in request.session:
    return redirect(index)
  user = User.objects.get(id=id)
  context = {
    "alias": user.alias,
    "name": user.name,
    "username": user.username
  }
  return render(request, 'djangobelt/user.html', context)
  
def removefriend(request, id):
  userid = request.session['userid']
  Friend.objects.filter(frienduser = id, befriender = userid).delete()
  return redirect('/dashboard')
  
  