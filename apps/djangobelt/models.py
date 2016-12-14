from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import re
import datetime
import bcrypt

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
    request.session['username'] = user.first_name + " " + user.last_name
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
    
    if not re.match(r"[a-zA-Z]{2,}",reg_info['fname']): # Alpha ONLY and 2 characters min.
      messages.error(request, "First Name: Must be at least 2 characters long.", extra_tags="register")
      errors = True
    if not re.match(r"[a-zA-Z]{2,}",reg_info['lname']): # Alpha ONLY and 2 characters min.
      messages.error(request, "Last Name: Must be at least 2 characters long.", extra_tags="register")
      errors = True
    if not re.match(r"[^@]+@[^@]+\.[^@]+",reg_info['email']): # Valid email address
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
      first_name = reg_info['fname'],
      last_name  = reg_info['lname'],
      username   = reg_info['email'],
      password   = securepass
    )

    user.save()
  
    if user.id != None:
      request.session['loggedin'] = True
      request.session['userid']   = user.id
      request.session['username'] = reg_info['fname'] + " " + reg_info['lname']
      return True
    else:
      return False


class User(models.Model):
  first_name = models.CharField(max_length=45)
  last_name  = models.CharField(max_length=45)
  birthday   = models.DateField(null=True, blank=True)
  username   = models.CharField(max_length=60)
  password   = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  
  objects = UserManager()

  