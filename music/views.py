# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
from django.shortcuts import render, get_object_or_404, render_to_response, get_list_or_404
from django.contrib.auth.models import User
from .models import Song, Album, Artist, Review
from django.db.models import Avg
from django import forms
from .forms import SearchForm, ReviewForm
import spotipy
import spotipy.oauth2 as oauth2

credentials = oauth2.SpotifyClientCredentials(
		client_id='SECRET',
		client_secret='SECRET')

token = credentials.get_access_token()
sp = spotipy.Spotify(auth=token)

def convertMillis(millis):
	mill = float(millis)
	seconds=(mill/1000)%60
	seconds = str(seconds)
	minutes=(mill/(1000*60))%60
	minutes = str(minutes)
	return minutes + ":" + seconds

def search(request):
	if request.GET:
		searchname = request.GET.get('q')
		if 'r' in request.GET:
			Song.objects.all().delete()
			Album.objects.all().delete()
			Artist.objects.all().delete()
			results = sp.search(q=searchname, limit=50, type='track')
			for i,t in enumerate(results['tracks']['items']):
				theTitle = t['name']
				theAlbum = t['album']['name']
				albumId = t['album']['id']
				theId = t['id']
				theType=t['type']
				thePreview = t['preview_url']
				theExternal = t['external_urls']['spotify']
				theURI = t['uri']
				theDuration = convertMillis(t['duration_ms'])
				theMainArtist = t['artists'][0]['name']
				somelist = [x['name'] for x in t['artists']]
				theArtists = ', '.join(somelist)
				thePopularity = float(t['popularity'])
				thatList = [str(x) for x in t['available_markets']]
				theMarkets = ', '.join(thatList)
				#print theTitle
				theImage = t['album']['images'][0]['url']
				theSong = Song.objects.create(title=theTitle,theType=theType,query=searchname,albumId=albumId,album=theAlbum,songId=theId,preview=thePreview,external=theExternal,uri=theURI,duration=theDuration,mainArtist=theMainArtist,artists=theArtists,popularity=thePopularity,image=theImage)
				musicData = Song.objects.filter(query=searchname)
		if 'j' in request.GET:
			Song.objects.all().delete()
			Album.objects.all().delete()
			Artist.objects.all().delete()
			results = sp.search(q=searchname, limit=50, type='track')
			for i,t in enumerate(results['tracks']['items']):
				theTitle = t['name']
				theAlbum = t['album']['name']
				theId = t['id']
				theType=t['type']
				thePreview = t['preview_url']
				theExternal = t['external_urls']['spotify']
				theURI = t['uri'] 
				theDuration = convertMillis(t['duration_ms'])
				theMainArtist = t['artists'][0]['name']
				somelist = [x['name'] for x in t['artists']]
				theArtists = ', '.join(somelist)
				thePopularity = t['popularity']
				thatList = [str(x) for x in t['available_markets']]
				theMarkets = ', '.join(thatList)
				theImage = t['album']['images'][0]['url']
				#print theTitle
				theSong = Song.objects.create(title=theTitle,theType=theType,query=searchname,album=theAlbum,songId=theId,preview=thePreview,external=theExternal,uri=theURI,duration=theDuration,mainArtist=theMainArtist,artists=theArtists,popularity=thePopularity,image=theImage)
				musicData = Song.objects.filter(query=searchname).order_by('-popularity')
		if 'p' in request.GET:
			Song.objects.all().delete()
			Album.objects.all().delete()
			Artist.objects.all().delete()
			results = sp.search(q=searchname, limit=50, type='album')
			for i,t in enumerate(results['albums']['items']):
				theTitle = t['name']
				theImage = t['images'][0]['url']
				theId = t['id']
				someting = sp.album(theId)
				releaseDate = someting['release_date']
				popularity = float(someting['popularity'])
				theType = someting['album_type']
				theExternal = t['external_urls']['spotify']
				theURI = t['uri']
				theMainArtist = t['artists'][0]['name']
				somelist = [x['name'] for x in t['artists']]
				theArtists = ', '.join(somelist)
				thatList = [str(x) for x in t['available_markets']]
				theMarkets = ', '.join(thatList)
				theAlbum = Album.objects.create(title=theTitle,theType=theType,popularity=popularity,releaseDate=releaseDate,query=searchname,image=theImage,albumId=theId,external=theExternal,uri=theURI,mainArtist=theMainArtist,artists=theArtists)
				musicData = Album.objects.filter(query=searchname)
		return render(request, 'search.html',{'musicData': musicData, 'search': True})
	else:
		return render(request, 'search.html')   

def song_page(request, song_id):
	track = sp.track(song_id)
	song_pg = Song.objects.get(songId=song_id)
	album = sp.album(track['album']['id'])
	print album.keys()
	albumId= album['id']
	somelist = [x['name'] for x in album['artists']]
	theArtists = ', '.join(somelist)
	print album['name']
	print album['images'][0]['url']
	print album['id']
	print album['external_urls']['spotify']
	print album['uri']
	if Album.objects.filter(albumId=albumId).exists():
		album_pg=Album.objects.get(albumId=albumId)
	else:
		theAlbum = Album.objects.create(title=album['name'],theType=album['album_type'],popularity=float(album['popularity']),releaseDate=album['release_date'],query='nothin',image=album['images'][0]['url'],albumId=album['id'],external=album['external_urls']['spotify'],uri=album['uri'],mainArtist=album['artists'][0]['name'],artists=theArtists)
		album_pg=Album.objects.get(albumId=albumId)
	return render_to_response('song.html',{'song_pg': song_pg, 'album_pg': album_pg})

def album_page(request, album_id):
	album_pg = Album.objects.get(albumId=album_id)
	j = sp.album_tracks(album_id, limit=50, offset=0)
	album = sp.album(album_id)
	albumName = album['name']
	for r in j['items']:
		#print r
		track = sp.track(r['id'])
		popularity = track['popularity']
		image = track['album']['images'][0]['url']
		somelist = [r['name'] for x in r['artists']]
		theArtists = ', '.join(somelist)
		if Song.objects.filter(songId=r['id']).exists():
			print 'hi'
			musicData = Song.objects.filter(albumId=album_id)
		else:
			theSong = Song.objects.create(title=r['name'],theType=r['type'],albumId=album_id,query='nothin',album=albumName,songId=r['id'],preview=r['preview_url'],external=r['external_urls']['spotify'],uri=r['uri'],duration=convertMillis(r['duration_ms']),mainArtist=r['artists'][0]['name'],artists=theArtists,popularity=popularity,image=image)
			musicData = Song.objects.filter(albumId=album_id)
	return render_to_response('album.html',{'album_pg': album_pg, 'musicData': musicData})



# Create your views here.
