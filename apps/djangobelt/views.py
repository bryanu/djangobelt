from django.shortcuts import render, redirect
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
