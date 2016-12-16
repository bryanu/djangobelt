from django.conf.urls import url
from .import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^login$', views.login),
  url(r'^register$', views.register),
  url(r'^logout$', views.logout),
  url(r'^dashboard$', views.friends),
  url(r'^befrienduser/(?P<id>\d+)$', views.befrienduser),
  url(r'^viewuser/(?P<id>\d+)$', views.viewuser),
  url(r'^removefriend/(?P<id>\d+)$', views.removefriend),
  
]
