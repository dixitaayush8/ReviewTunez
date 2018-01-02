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
				artistId = t['artists'][0]['id']
				theImage = t['album']['images'][0]['url']
				theSong = Song.objects.create(title=theTitle,theType=theType,query=searchname,albumId=albumId,album=theAlbum,songId=theId,preview=thePreview,external=theExternal,uri=theURI,duration=theDuration,mainArtist=theMainArtist,artists=theArtists,popularity=thePopularity,image=theImage,artistId=artistId)
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
				artistId = t['artists'][0]['id']
				#print theTitle
				theSong = Song.objects.create(title=theTitle,theType=theType,query=searchname,album=theAlbum,songId=theId,preview=thePreview,external=theExternal,uri=theURI,duration=theDuration,mainArtist=theMainArtist,artists=theArtists,popularity=thePopularity,image=theImage,artistId=artistId)
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
		if 'n' in request.GET:
			Song.objects.all().delete()
			Album.objects.all().delete()
			Artist.objects.all().delete()
			results = sp.search(q=searchname, limit=50, type='artist')
			for i,t in enumerate(results['artists']['items']):
				name = t['name']
				artistId = t['id']
				genres = [x for x in t['genres']]
				theGenres = ', '.join(genres)
				external = t['external_urls']['spotify']
				uri = t['uri']
				if not t['images']:
					image = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
				else:
					image = t['images'][0]['url']
				#image = t['images'][0]['url']
				popularity = float(t['popularity'])
				numOfFollowers = t['followers']
				theArtist = Artist.objects.create(name=name,query=searchname,artistId=artistId,genres=theGenres,external=external,uri=uri,image=image,popularity=popularity,numOfFollowers=numOfFollowers,songId="None",albumId="None")
				musicData = Artist.objects.filter(query=searchname)
		return render(request, 'search.html',{'musicData': musicData, 'search': True})
	else:
		return render(request, 'search.html')   

def song_page(request, song_id):
	theTrack = sp.track(song_id)
	if Song.objects.filter(songId=song_id).exists():
		song_pg = Song.objects.get(songId=song_id)
	else:
		theSong = Song.objects.create(title=theTrack['name'],theType=theTrack['type'],query='nothing',album=theTrack['album']['name'],songId=theTrack['id'],preview=theTrack['preview_url'],external=theTrack['external_urls']['spotify'],uri=theTrack['uri'],duration=convertMillis(theTrack['duration_ms']),mainArtist=theTrack['artists'][0]['name'],artists='nope',popularity=theTrack['popularity'],image=theTrack['album']['images'][0]['url'],artistId=theTrack['artists'][0]['id'])
		song_pg = Song.objects.get(songId=song_id)
	Artist.objects.all().delete()
	track = sp.track(song_id)
	#song_pg = Song.objects.get(songId=song_id)
	album = sp.album(track['album']['id'])
	albumId= album['id']
	for r in track['artists']:
		l = sp.artist(r['id'])
		genres = [x for x in l['genres']]
		theGenres = ', '.join(genres)
		if not l['images']:
			image = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
		else:
			image = l['images'][0]['url']
		if Artist.objects.filter(artistId=l['id']).exists():
			artistData = Artist.objects.filter(songId=song_id)
		else:
			theArtist = Artist.objects.create(name=l['name'],query='nothing',artistId=l['id'],genres=theGenres,external=l['external_urls']['spotify'],uri=l['uri'],image=image,popularity=l['popularity'],numOfFollowers=l['followers'],songId=song_id,albumId="None")
			artistData = Artist.objects.filter(songId=song_id)
	somelist = [x['name'] for x in album['artists']]
	theArtists = ', '.join(somelist)
	if Album.objects.filter(albumId=albumId).exists():
		album_pg=Album.objects.get(albumId=albumId)
	else:
		theAlbum = Album.objects.create(title=album['name'],theType=album['album_type'],popularity=float(album['popularity']),releaseDate=album['release_date'],query='nothin',image=album['images'][0]['url'],albumId=album['id'],external=album['external_urls']['spotify'],uri=album['uri'],mainArtist=album['artists'][0]['name'],artists=theArtists)
		album_pg=Album.objects.get(albumId=albumId)
	return render_to_response('song.html',{'song_pg': song_pg, 'album_pg': album_pg, 'artist_pg': artistData})

def album_page(request, album_id):
	Song.objects.all().delete()
	Artist.objects.all().delete()
	album_pg = Album.objects.get(albumId=album_id)
	j = sp.album_tracks(album_id, limit=50, offset=0)
	album = sp.album(album_id)
	albumName = album['name']
	for i in album['artists']:
		y = sp.artist(i['id'])
		genres = [x for x in y['genres']]
		theGenres = ', '.join(genres)
		if not y['images']:
			image = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
		else:
			image = y['images'][0]['url']
		if Artist.objects.filter(artistId=y['id']).exists():
			artistData = Artist.objects.filter(albumId=album_id)
		else:
			theArtist = Artist.objects.create(name=y['name'],query='nothing',artistId=y['id'],genres=theGenres,external=y['external_urls']['spotify'],uri=y['uri'],image=image,popularity=y['popularity'],numOfFollowers=y['followers'],songId="None",albumId=album_id)
			artistData = Artist.objects.filter(albumId=album_id)
	for r in j['items']:
		#print r
		track = sp.track(r['id'])
		popularity = track['popularity']
		image = track['album']['images'][0]['url']
		somelist = [x['name'] for x in track['artists']]
		#print somelist
		theArtists = ', '.join(somelist)
		if Song.objects.filter(songId=r['id']).exists():
			musicData = Song.objects.filter(albumId=album_id)
		else:
			theSong = Song.objects.create(title=r['name'],theType=r['type'],albumId=album_id,query='nothin',album=albumName,songId=r['id'],preview=r['preview_url'],external=r['external_urls']['spotify'],uri=r['uri'],duration=convertMillis(r['duration_ms']),mainArtist=r['artists'][0]['name'],artists=theArtists,popularity=popularity,image=image,artistId=r['artists'][0]['id'])
			musicData = Song.objects.filter(albumId=album_id)
	return render_to_response('album.html',{'album_pg': album_pg, 'musicData': musicData, 'artist_pg': artistData})

def artist_page(request, artist_id):
	Song.objects.all().delete()
	artist_pg = Artist.objects.get(artistId=artist_id)
	top = sp.artist_top_tracks(artist_id,country='US')
	if not top['tracks']:
		songData = 'nothin'
	else:
		print len(top['tracks'])
		for i in top['tracks'][:10]:
			somelist = [x['name'] for x in i['artists']]
			theArtists = ', '.join(somelist)
			if Song.objects.filter(songId=i['id']).exists():
				songData = Song.objects.filter(artistId=artist_id)
			else:
				theSong = Song.objects.create(title=i['name'],theType=i['type'],albumId=i['album']['id'],query='nah',album=i['album']['name'],songId=i['id'],preview=i['preview_url'],external=i['external_urls']['spotify'],uri=i['uri'],duration=convertMillis(i['duration_ms']),mainArtist=i['artists'][0]['name'],artists=theArtists,popularity=i['popularity'],image=i['album']['images'][0]['url'],artistId=artist_id)
				songData = Song.objects.filter(artistId=artist_id)
	return render_to_response('artist.html', {'artist_pg': artist_pg, 'songData': songData})



# Create your views here.
