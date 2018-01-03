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
	popularity = models.FloatField(max_length=101, default=0)
	image = models.CharField(max_length=100, default='None', null=True, blank=True)
	theType = models.CharField(max_length = 10, default='No type')
	albumId = models.CharField(max_length=100, default='None')
	artistId = models.CharField(max_length=100, default='None')
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
	releaseDate = models.CharField(max_length=20, default='No release date', null=True, blank=True)
	popularity = models.FloatField(max_length=101, default=0)
	theType = models.CharField(max_length = 10, default='No type')
	artistId = models.CharField(max_length=100, default='None')
	#access API docs to get list of tracks

class Artist(models.Model):
	genres = models.CharField(max_length=100, default='No genres')
	query = models.CharField(max_length=100, default='No query')
	name = models.CharField(max_length=100, default='No name')
	artistId = models.CharField(max_length=100, primary_key=True)
	external = models.CharField(max_length=100, default='No external URL')
	uri = models.CharField(max_length=100, default='No URI')
	image = models.CharField(max_length=100, default='No image')
	popularity = models.FloatField(max_length=101, default=0)
	numOfFollowers = models.CharField(max_length=20,default="0")
	songId = models.CharField(max_length=30, default="None", null=True, blank=True)
	albumId = models.CharField(max_length = 30, default="None", null=True, blank=True)
	#tracks = models.ManyToManyField(Song)
	#topTenTracks = models.CharField(max_length=1000, default="No top tracks") #access API docs to generate
	#albums = models.CharField(max_length=1000, default="No albums") #access API docs to generate
	#related artists, use API docs

class SongReview(models.Model):
	songId = models.CharField(max_length=10, default='No song', null=True, blank=True)
	#albumId = models.CharField(max_length=10, default='No album', null=True, blank=True)
	#artistId = models.CharField(max_length=10, default='No artist', null=True, blank=True)
	user = models.ForeignKey(User)
	comment = models.CharField(max_length = 500, default='No comment')
	songTitle = models.CharField(max_length=100, default='No song title', null=True, blank=True)
	#albumTitle = models.CharField(max_length=100, default='No album title', null=True, blank=True)
	#artistTitle = models.CharField(max_length=100, default='No artist title', null=True, blank=True)
	songArtists = models.CharField(max_length=10, default='No artists', null=True, blank=True)
	rating = models.FloatField(max_length=2, default=1)
	time = models.CharField(max_length=15, default='No date')

class AlbumReview(models.Model):
	albumId = models.CharField(max_length=10, default='No album', null=True, blank=True)
	albumTitle = models.CharField(max_length=100, default='No song title', null=True, blank=True)
	user = models.ForeignKey(User)
	comment = models.CharField(max_length = 500, default='No comment')
	albumArtists = models.CharField(max_length=10,default='No artists',null=True,blank=True)
	rating = models.FloatField(max_length = 2, default=1)
	time = models.CharField(max_length=15, default='No date')

class ArtistReview(models.Model):
	artistId = models.CharField(max_length=10, default='No artist', null=True, blank=True)
	user = models.ForeignKey(User)
	comment = models.CharField(max_length = 500, default='No comment')
	artistName = models.CharField(max_length=10,default='No artist',null=True,blank=True)
	rating = models.FloatField(max_length = 2, default=1)
	time = models.CharField(max_length=15, default='No date')
# Create your models here.
