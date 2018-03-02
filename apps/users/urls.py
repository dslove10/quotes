from django.conf.urls import url 
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^create$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^quotes$', views.quotes),
	url(r'^quotes/add$', views.add),
	url(r'^users/(?P<number>\d+)$', views.info),
	url(r'^quotes/add_quote/(?P<number>\d+)$', views.add_quote),
	url(r'^quotes/remove/(?P<number>\d+)$', views.remove)
]