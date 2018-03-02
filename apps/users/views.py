# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import F
from .models import *
import bcrypt

# Create your views here.
def index(request):
	return render(request, 'users/index.html')

def register(request):
	errors = User.objects.register_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/')
	else:
		hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		new_user = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed_pw, dob = request.POST['dob'])
		user = User.objects.get(email = request.POST['email'])
		request.session['alias'] = user.alias
		request.session['id'] = user.id
		return redirect('/quotes')

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/')
	else:
		user = User.objects.get(email = request.POST['email'])
		request.session['alias'] = user.alias
		request.session['id'] = user.id
		return redirect('/quotes')

def logout(request):
	del request.session['alias']
	del request.session['id']
	return redirect('/')

def quotes(request):
	quote_list = {
		'fav_quotes': Quote.objects.filter(users = User.objects.get(id = request.session['id'])),
		'all_quotes': Quote.objects.exclude(users = User.objects.get(id = request.session['id']))
	}
	return render(request, 'users/quotes.html', quote_list)

def add(request):
	errors = Quote.objects.quote_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/quotes')
	else:
		quote = Quote.objects.create(author = request.POST['author'], quote = request.POST['quote'], quote_creator = User.objects.get(id = request.session['id']))
		this_user = User.objects.get(id = request.session['id'])
		this_user.quotes.add(Quote.objects.get(quote = request.POST['quote']))
		return redirect('/quotes')

def info(request, number):
	request.session['user'] = User.objects.get(id = number).name
	context = {
		'quote_count': Quote.objects.filter(quote_creator_id = number).count(),
		'this_user': Quote.objects.filter(quote_creator_id =  number)
	}
	return render(request, 'users/user.html', context)

def add_quote(request, number):
	this_user = User.objects.get(id = request.session['id'])
	this_user.quotes.add(Quote.objects.get(id = number))
	return redirect('/quotes')

def remove(request, number):
	this_user = User.objects.get(id = request.session['id'])
	this_user.quotes.remove(Quote.objects.get(id = number))
	return redirect('/quotes')