# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class Song(models.Model):
	title = models.CharField(max_length=100, default='No song title')
	query = models.CharField(max_length=100, default='No query')
	album = models.CharField(max_length=100, default='No album')
	songId = models.CharField(max_length=100, primary_key=True)
	preview = models.CharField(max_length=100, default='None', null=True, blank=True)
	external = models.CharField(max_length=100, default='No external URL')
	uri = models.CharField(max_length=100, default='No URI')
	duration = models.CharField(max_length=10, default='No duration')
	mainArtist = models.CharField(max_length=20, default='No artist')
	artists = models.CharField(max_length=20, default='No artists')
	popularity = models.CharField(max_length=3, default="0")
	markets = models.CharField(max_length=100, default='No available markets')
	image = models.CharField(max_length=100, default='None', null=True, blank=True)
	#recommendations, use API docs

class Album(models.Model):
	title = models.CharField(max_length=100, default='No album title')
	query = models.CharField(max_length=100, default='No query')
	image = models.CharField(max_length=200, default='No image')
	albumId = models.CharField(max_length=100, primary_key=True)
	external = models.CharField(max_length=100, default='No external URL')
	uri = models.CharField(max_length=100, default='No URI')
	mainArtist = models.CharField(max_length=20, default='No artist')
	artists = models.CharField(max_length=20, default='No artists')
	markets = models.CharField(max_length=100, default='No available markets')
	tracks = models.CharField(max_length = 1000, default='No tracks') #access API docs to get list of tracks

class Artist(models.Model):
	genres = models.CharField(max_length=100, default='No genres')
	name = models.CharField(max_length=100, default='No name')
	artistId = models.CharField(max_length=100, primary_key=True)
	external = models.CharField(max_length=100, default='No external URL')
	uri = models.CharField(max_length=100, default='No URI')
	image = models.CharField(max_length=100, default='No image')
	popularity = models.CharField(max_length=3, default="0")
	numOfFollowers = models.CharField(max_length=20,default="0")
	topTenTracks = models.CharField(max_length=1000, default="No top tracks") #access API docs to generate
	albums = models.CharField(max_length=1000, default="No albums") #access API docs to generate
	#related artists, use API docs

class Review(models.Model):
	songId = models.CharField(max_length=10, default='No song', null=True, blank=True)
	albumId = models.CharField(max_length=10, default='No album', null=True, blank=True)
	artistId = models.CharField(max_length=10, default='No artist', null=True, blank=True)
	user = models.ForeignKey(User)
	comment = models.CharField(max_length = 500, default='No comment')
	songTitle = models.CharField(max_length=100, default='No song title', null=True, blank=True)
	albumTitle = models.CharField(max_length=100, default='No album title', null=True, blank=True)
	artistTitle = models.CharField(max_length=100, default='No artist title', null=True, blank=True)
	songArtists = models.CharField(max_length=10, default='No artists', null=True, blank=True)
	rating = models.FloatField(max_length=2, default=1)

# Create your models here.
