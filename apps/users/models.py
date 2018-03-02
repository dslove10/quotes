# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z_ ]*$')

# Create your models here.
class UserManager(models.Manager):
	def register_validator(self, postData):
		errors = {}
		if len(postData['name']) < 3:
			errors["name"] = 'Name must be at least 2 characters'
		if not NAME_REGEX.match(postData['name']):
			errors["name"] = 'Only letters, underscore, or spaces allowed for name'
		if len(postData['alias']) < 3:
			errors["alias"] = 'Alias must be at least 2 characters'
		if User.objects.filter(alias = postData['alias']).exists():
			errors["alias"] = 'Alias already exists'
		if len(postData['email']) < 1:
			errors["email"] = 'Email cannot be empty'
		if not EMAIL_REGEX.match(postData['email']):
			errors["email"] = 'Must be a valid email'
		if User.objects.filter(email = postData['email']).exists():
			errors["email"] = 'Email already exists'
		if len(postData['password']) < 8:
			errors["password"] = 'Password must be at least 8 characters'
		if postData['password'] != postData['confirm']:
			errors["password"] = 'Passwords do not match'
		today = datetime.today().strftime('%Y %m %d')
		if postData['dob'] > today:
			errors["time"] = "Date must be before today's date"
		return errors

	def login_validator(self, postData):
		no_user = User.objects.filter(email = postData['email'])
		errors = {}
		if len(no_user) == 0:
			errors['no_user'] = 'Invalid Email/Password Combination'
		elif postData['email'] == User.objects.get(email = postData['email']).email:
			db_pass = User.objects.get(email = postData['email']).password
			if bcrypt.checkpw(postData['password'].encode(), db_pass.encode()) == False:
				errors["pass_check"] = 'Invalid Email/Password Combination'
		return errors

class QuoteManager(models.Manager):
	def quote_validator(self, postData):
		errors = {}
		if len(postData['author']) < 3:
			errors["author"] = 'Quote author must be at least 3 characters'
		if len(postData['quote']) < 10:
			errors["quote"] = 'Quote must be at least 10 characters'
		if Quote.objects.filter(quote = postData['quote']).exists():
			errors["quote"] = 'This quote already exists'
		return errors


class User(models.Model):
	name = models.CharField(max_length = 255)
	alias = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.TextField()
	dob = models.DateField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = UserManager()

class Quote(models.Model):
	author = models.CharField(max_length = 255)
	quote = models.TextField(max_length = 1000)
	quote_creator = models.ForeignKey(User, related_name = 'quote_created')
	users = models.ManyToManyField(User, related_name = 'quotes')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = QuoteManager()