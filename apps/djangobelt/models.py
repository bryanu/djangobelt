from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db import models
import re
import bcrypt
import datetime

class UserManager(models.Manager):

  def login(self, request, email, password):
    try:
      user = User.objects.get(username=email)
    except self.model.DoesNotExist:
      messages.error(request, "email/password combination is incorrect!", extra_tags="login")
      return False

    pwcheck = bcrypt.hashpw(password.encode('utf-8'), user.password.encode('utf-8'))

    if pwcheck != user.password:
      request.session['loggedin'] = False
      request.session['userid']   = 0
      request.session['username'] = ""
      return False
    request.session['loggedin'] = True
    request.session['userid']   = user.id
    request.session['username'] = user.name
    return True
  

  def logout(self, request):
    if not 'loggedin' in request.session:
      return False
    request.session.pop('loggedin')
    request.session.pop('userid')
    request.session.pop('username')
    return True

  
  def register(self, request, reg_info):
    errors = False
    
    if not re.match(r"[a-zA-Z]{2,}",reg_info['name']): # Alpha ONLY and 2 characters min.
      messages.error(request, "First Name: Must be at least 2 characters long.", extra_tags="register")
      errors = True
    if not re.match(r"[a-zA-Z]{2,}",reg_info['alias']): # Alpha ONLY and 2 characters min.
      messages.error(request, "Last Name: Must be at least 2 characters long.", extra_tags="register")
      errors = True
      
    
#    if not re.match(r"\d{2}[-/]\d{2}[-/]\d{4}",reg_info['birthdate']): # Valid email address
#      messages.error(request, "Please enter a valid birthdate (mm/dd/yyyy)", extra_tags="register")
#      errors = True
      
      
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",reg_info['email']): # Valid email address
      messages.error(request, "Email: Must be a valid email address.", extra_tags="register")
      errors = True
    if not re.match(r"[a-zA-Z0-9]{8,}",reg_info['password']): # Alpha-Numberic - 8 characters min.
      messages.error(request, "Password: Must be at least 8 characters long, and only alpha-numberic characters.", extra_tags="register")
      errors = True
    if reg_info['password'] != reg_info['password2']: # Passwords must match
      messages.error(request, "Confirmation Password: Must match password entered.", extra_tags="register")
      errors = True

    if errors:
      return False

    securepass = bcrypt.hashpw(reg_info['password'].encode('utf-8'), bcrypt.gensalt())

    user = User.objects.create(
      name       = reg_info['name'],
      alias      = reg_info['alias'],
      username   = reg_info['email'],
      birthdate  = reg_info['birthdate'],
      password   = securepass
    )

    user.save()
  
    if user.id != None:
      request.session['loggedin'] = True
      request.session['userid']   = user.id
      request.session['username'] = reg_info['name']
      return True
    else:
      return False


class User(models.Model):
  name       = models.CharField(max_length=45)
  alias      = models.CharField(max_length=45)
  username   = models.CharField(max_length=45)
  password   = models.CharField(max_length=100)
  birthdate  = models.DateTimeField(auto_now_add=False)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  objects    = UserManager()

  
class FriendManager(models.Manager):
  def friend(self, user_id, friend_id):
    user        = User.objects.get(id = user_id)
    friend_user = User.objects.get(id = friend_id)
    self.create(frienduser=friend_user, befriender=user)
    return True
  
class Friend(models.Model):
  frienduser = models.ForeignKey(User, related_name='friend_user')
  befriender = models.ForeignKey(User, related_name='befriender')
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = FriendManager()

  
  