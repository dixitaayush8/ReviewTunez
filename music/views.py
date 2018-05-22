# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from time import gmtime, localtime, strftime
import random
from django.shortcuts import render, get_object_or_404, render_to_response, get_list_or_404
from django.contrib.auth.models import User
from .models import Song, Album, Artist, SongReview, AlbumReview, ArtistReview
from django.db.models import Avg
from django import forms
from .forms import SearchForm, ReviewForm
from apiclient.discovery import build
import unicodedata
import spotipy
import spotipy.oauth2 as oauth2
from bs4 import BeautifulSoup
import requests
import urllib

credentials = oauth2.SpotifyClientCredentials(
		client_id='SECRET',
		client_secret='SECRET')

DEVELOPER_KEY = 'SECRET'
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
# credentials = oauth2.SpotifyClientCredentials(
# 		client_id='SECRET',
# 		client_secret='SECRET')

# token = credentials.get_access_token()


# sp = spotipy.Spotify(auth=token)

#sp = spotipy.Spotify(client_credentials_manager=credentials)duration


def search(request):
	token = credentials.get_access_token()
	sp = spotipy.Spotify(auth=token)
	musicData = 'there is an error'
	if request.GET:
		searchname = request.GET.get('q')
		if 'r' in request.GET:
			Song.objects.all().delete()
			Album.objects.all().delete()
			Artist.objects.all().delete()
			try:
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
					theMainArtist = t['artists'][0]['name']
					somelist = [x['name'] for x in t['artists']]
					theArtists = ', '.join(somelist)
					thePopularity = float(t['popularity'])
					thatList = [str(x) for x in t['available_markets']]
					theMarkets = ', '.join(thatList)
					artistId = t['artists'][0]['id']
					if not t['album']['images']:
						theImage = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
					else:
						theImage = t['album']['images'][0]['url']
					theSong = Song.objects.create(title=theTitle,theType=theType,query=searchname,albumId=albumId,album=theAlbum,songId=theId,preview=thePreview,external=theExternal,uri=theURI,duration='none',mainArtist=theMainArtist,artists=theArtists,popularity=thePopularity,image=theImage,artistId=artistId)
					musicData = Song.objects.filter(query=searchname)
			except:
				musicData = "there is a song error"
		if 'j' in request.GET:
			Song.objects.all().delete()
			Album.objects.all().delete()
			Artist.objects.all().delete()
			try:
				results = sp.search(q=searchname, limit=50, type='track')
				for i,t in enumerate(results['tracks']['items']):
					theTitle = t['name']
					theAlbum = t['album']['name']
					theId = t['id']
					theType=t['type']
					thePreview = t['preview_url']
					theExternal = t['external_urls']['spotify']
					theURI = t['uri'] 
					theMainArtist = t['artists'][0]['name']
					somelist = [x['name'] for x in t['artists']]
					theArtists = ', '.join(somelist)
					thePopularity = t['popularity']
					thatList = [str(x) for x in t['available_markets']]
					theMarkets = ', '.join(thatList)
					if not t['album']['images']:
						theImage = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
					else:
						theImage = t['album']['images'][0]['url']
					artistId = t['artists'][0]['id']
					theSong = Song.objects.create(title=theTitle,theType=theType,query=searchname,album=theAlbum,songId=theId,preview=thePreview,external=theExternal,uri=theURI,duration='none',mainArtist=theMainArtist,artists=theArtists,popularity=thePopularity,image=theImage,artistId=artistId)
					musicData = Song.objects.filter(query=searchname).order_by('-popularity')
			except:
				musicData = "there is a song error"
		if 'p' in request.GET:
			Song.objects.all().delete()
			Album.objects.all().delete()
			Artist.objects.all().delete()
			try:
				results = sp.search(q=searchname, limit=10, type='album')
				for i,t in enumerate(results['albums']['items']):
					theTitle = t['name']
					print t['name']
					if not t['images']:
						theImage = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
					else:
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
					stringDate = unicodedata.normalize('NFKD', releaseDate).encode('ascii','ignore')
					theYear = stringDate[:4]
					theAlbum = Album.objects.create(year=theYear,title=theTitle,theType=theType,popularity=popularity,releaseDate=releaseDate,query=searchname,image=theImage,albumId=theId,external=theExternal,uri=theURI,mainArtist=theMainArtist,artists=theArtists,artistId='no')
					musicData = Album.objects.filter(query=searchname)
			except:
				musicData = "there is a album error"
		if 'yo' in request.GET:
			Song.objects.all().delete()
			Album.objects.all().delete()
			Artist.objects.all().delete()
			try:
				results = sp.search(q=searchname, limit=10, type='album')
				for i,t in enumerate(results['albums']['items']):
					theTitle = t['name']
					#print t['name']
					if not t['images']:
						theImage = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
					else:
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
					stringDate = unicodedata.normalize('NFKD', releaseDate).encode('ascii','ignore')
					theYear = stringDate[:4]
					theAlbum = Album.objects.create(year=theYear,title=theTitle,theType=theType,popularity=popularity,releaseDate=releaseDate,query=searchname,image=theImage,albumId=theId,external=theExternal,uri=theURI,mainArtist=theMainArtist,artists=theArtists,artistId='no')
					musicData = Album.objects.filter(query=searchname).order_by('-popularity')
			except:
				musicData = "there is a album error"
		if 'n' in request.GET:
			Song.objects.all().delete()
			Album.objects.all().delete()
			Artist.objects.all().delete()
			try:
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
					popularity = float(t['popularity'])
					numOfFollowers = t['followers']
					theArtist = Artist.objects.create(name=name,query=searchname,artistId=artistId,genres=theGenres,external=external,uri=uri,image=image,popularity=popularity,numOfFollowers=numOfFollowers,songId="None",albumId="None")
					musicData = Artist.objects.filter(query=searchname)
			except:
				musicData = "there is a artist error"
		if 'b' in request.GET:
			Song.objects.all().delete()
			Album.objects.all().delete()
			Artist.objects.all().delete()
			try:
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
					popularity = float(t['popularity'])
					numOfFollowers = t['followeres']
					theArtist = Artist.objects.create(name=name,query=searchname,artistId=artistId,genres=theGenres,external=external,uri=uri,image=image,popularity=popularity,numOfFollowers=numOfFollowers,songId="None",albumId="None")
					musicData = Artist.objects.filter(query=searchname).order_by('-popularity')
			except:
				musicData = "there is a artist error"
		return render(request, 'search.html',{'musicData': musicData, 'search': True})
	else:
		return render(request, 'search.html')   

def song_page(request, song_id):
	token = credentials.get_access_token()
	sp = spotipy.Spotify(auth=token)
	theUser = request.user
	allReviews = SongReview.objects.filter(songId=song_id).order_by('-time')
	average = allReviews.aggregate(Avg('rating'))
	theTrack = sp.track(song_id)
	songArtistLists = [x['name'] for x in theTrack['artists']]
	songArtists = ", ".join(songArtistLists)
	youtubeSearch = theTrack['artists'][0]['name'] + " " + theTrack['name']
	youtubeSearchString = youtubeSearch.encode('ascii','ignore')
	if "&" in youtubeSearchString:
		youtubeSearchString = youtubeSearchString.replace("&","%26")
	if "- From" in youtubeSearchString:
		index = youtubeSearchString.find("- From")
		youtubeSearchString = youtubeSearchString[:index]
	youtubeParsed = "+".join(youtubeSearchString.split())
	youtubeParsed = youtubeParsed.encode('ascii','ignore')
	if Song.objects.filter(songId=song_id).exists():
		song_pg = Song.objects.get(songId=song_id)
	else:
		theSong = Song.objects.create(title=theTrack['name'],theType=theTrack['type'],query='nothing',album=theTrack['album']['name'],songId=theTrack['id'],preview=theTrack['preview_url'],external=theTrack['external_urls']['spotify'],uri=theTrack['uri'],duration='none',mainArtist=theTrack['artists'][0]['name'],artists='nope',popularity=theTrack['popularity'],image=theTrack['album']['images'][0]['url'],artistId=theTrack['artists'][0]['id'])
		song_pg = Song.objects.get(songId=song_id)
	Artist.objects.all().delete()
	track = sp.track(song_id)
	album = sp.album(track['album']['id'])
	stringDate = unicodedata.normalize('NFKD', album['release_date']).encode('ascii','ignore')
	theYear = stringDate[:4]
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
		theAlbum = Album.objects.create(year=theYear,title=album['name'],theType=album['album_type'],popularity=float(album['popularity']),releaseDate=album['release_date'],query='nothin',image=album['images'][0]['url'],albumId=album['id'],external=album['external_urls']['spotify'],uri=album['uri'],mainArtist=album['artists'][0]['name'],artists=theArtists,artistId='no')
		album_pg=Album.objects.get(albumId=albumId)
	if not allReviews:
		allReviews = 'nope'
	if request.GET:
		theComment = request.GET.get('review')
		theRating = request.GET.get('number')
		if 'reviewed' in request.GET:
			showtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
			theReview = SongReview.objects.create(songId=song_id,albumId=theTrack['album']['id'],albumTitle=theTrack['album']['name'],image=theTrack['album']['images'][0]['url'],time=showtime, songTitle=theTrack['name'],songArtists=songArtists,user=theUser,comment=theComment,rating=theRating)
			allReviews = SongReview.objects.filter(songId=song_id).order_by('-time')
			average = allReviews.aggregate(Avg('rating'))
			return render_to_response('song.html',{'song_pg': song_pg, 'youtubeParsed': youtubeParsed, 'theUser': theUser, 'average': average, "allReviews": allReviews, 'album_pg': album_pg, 'artist_pg': artistData})
	else:
		return render_to_response('song.html',{'song_pg': song_pg, 'youtubeParsed': youtubeParsed, 'theUser': theUser, 'average': average, "allReviews": allReviews, 'album_pg': album_pg, 'artist_pg': artistData})

def album_page(request, album_id):
	token = credentials.get_access_token()
	sp = spotipy.Spotify(auth=token)
	Song.objects.all().delete()
	Artist.objects.all().delete()
	theUser = request.user
	allReviews = AlbumReview.objects.filter(albumId=album_id)
	average = allReviews.aggregate(Avg('rating'))
	album = sp.album(album_id)
	stringDate = unicodedata.normalize('NFKD', album['release_date']).encode('ascii','ignore')
	theYear = stringDate[:4]
	somelist = [x['name'] for x in album['artists']]
	theAlbumArtists = ', '.join(somelist)
	if Album.objects.filter(albumId=album_id).exists():
		album_pg=Album.objects.get(albumId=album_id)
	else:
		theAlbum = Album.objects.create(year=theYear,title=album['name'],theType=album['album_type'],popularity=float(album['popularity']),releaseDate=album['release_date'],query='nothin',image=album['images'][0]['url'],albumId=album['id'],external=album['external_urls']['spotify'],uri=album['uri'],mainArtist=album['artists'][0]['name'],artists=theAlbumArtists,artistId='no')
		album_pg=Album.objects.get(albumId=album_id)
	j = sp.album_tracks(album_id, limit=50, offset=0)
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
		track = sp.track(r['id'])
		popularity = track['popularity']
		if not track['album']['images']:
			image = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
		else:
			image = track['album']['images'][0]['url']
		somelist = [x['name'] for x in track['artists']]
		theArtists = ', '.join(somelist)
		if Song.objects.filter(songId=r['id']).exists():
			musicData = Song.objects.filter(albumId=album_id)
		else:
			theSong = Song.objects.create(title=r['name'],theType=r['type'],albumId=album_id,query='nothin',album=albumName,songId=r['id'],preview=r['preview_url'],external=r['external_urls']['spotify'],uri=r['uri'],duration='none',mainArtist=r['artists'][0]['name'],artists=theArtists,popularity=popularity,image=image,artistId=r['artists'][0]['id'])
			musicData = Song.objects.filter(albumId=album_id)
	if not allReviews:
		allReviews = 'nope'
	if request.GET:
		theComment = request.GET.get('review')
		theRating = request.GET.get('number')
		if 'reviewed' in request.GET:
			showtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
			theReview = AlbumReview.objects.create(albumId=album_id,image=album['images'][0]['url'],time=showtime,albumTitle=album['name'],albumArtists=theAlbumArtists,user=theUser,comment=theComment,rating=theRating)
			allReviews = AlbumReview.objects.filter(albumId=album_id)
			average = allReviews.aggregate(Avg('rating'))
			return render_to_response('album.html',{'album_pg': album_pg, 'theUser': theUser, 'average': average, 'allReviews': allReviews, 'musicData': musicData, 'artist_pg': artistData})
	else:
		return render_to_response('album.html',{'album_pg': album_pg, 'theUser': theUser, 'average': average, 'allReviews': allReviews, 'musicData': musicData, 'artist_pg': artistData})


def artist_page(request, artist_id):
	token = credentials.get_access_token()
	sp = spotipy.Spotify(auth=token)
	Song.objects.all().delete()
	Album.objects.all().delete()
	theUser = request.user
	ta = sp.artist(artist_id)
	allReviews = ArtistReview.objects.filter(artistId=artist_id)
	average = allReviews.aggregate(Avg('rating'))
	if not ta['images']:
		image = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
	else:
		image = ta['images'][0]['url']
	if Artist.objects.filter(artistId=artist_id).exists():
		artist_pg = Artist.objects.get(artistId = artist_id)
	else:
		genres = [x for x in ta['genres']]
		theGenres = ', '.join(genres)
		artistData = Artist.objects.create(name=ta['name'],query='nothin',artistId=ta['id'],genres=theGenres,external=ta['external_urls']['spotify'],uri=ta['uri'],image=image,popularity=ta['popularity'],numOfFollowers=ta['followers'],songId="None",albumId="none")
		artist_pg = Artist.objects.get(artistId=artist_id)
	top = sp.artist_top_tracks(artist_id,country='US')
	if not top['tracks']:
		songData = 'nothin'
	else:
		for i in top['tracks'][:10]:
			somelist = [x['name'] for x in i['artists']]
			theArtists = ', '.join(somelist)
			if Song.objects.filter(songId=i['id']).exists():
				songData = Song.objects.filter(artistId=artist_id)
			else:
				theSong = Song.objects.create(title=i['name'],theType=i['type'],albumId=i['album']['id'],query='nah',album=i['album']['name'],songId=i['id'],preview=i['preview_url'],external=i['external_urls']['spotify'],uri=i['uri'],duration='none',mainArtist=i['artists'][0]['name'],artists=theArtists,popularity=i['popularity'],image=i['album']['images'][0]['url'],artistId=artist_id)
				songData = Song.objects.filter(artistId=artist_id)
	albums = sp.artist_albums(artist_id,country='US',album_type='album',limit=50)
	#print albums
	if not albums['items']:
		albumData = 'nothin'
	else:
		for album in albums['items']:
			#print album['id']
			if Album.objects.filter(albumId=album['id']).exists():
				album_pg=Album.objects.filter(artistId=artist_id)
			else:
				someAlbum = sp.album(album['id'])
				somelist = [x['name'] for x in album['artists']]
				theArtists = ', '.join(somelist)
				stringDate = unicodedata.normalize('NFKD', someAlbum['release_date']).encode('ascii','ignore')
				theYear = stringDate[:4]
				if not album['images']:
					theImage = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
				else:
					theImage = album['images'][0]['url']
				#print album['name']
				#print theArtists
				theAlbum = Album.objects.create(year=theYear,title=album['name'],theType=album['album_type'],popularity=float(someAlbum['popularity']),releaseDate=someAlbum['release_date'],query='nothin',image=theImage,albumId=album['id'],external=album['external_urls']['spotify'],uri=album['uri'],mainArtist=album['artists'][0]['name'],artists=theArtists,artistId=artist_id)
				albumData = Album.objects.filter(artistId=artist_id)
	if not allReviews:
		allReviews = 'nope'
	if request.GET:
		theComment = request.GET.get('review')
		theRating = request.GET.get('number')
		if 'reviewed' in request.GET:
			showtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
			theReview = ArtistReview.objects.create(artistId=artist_id,image=image,user=theUser,comment=theComment,rating=theRating,artistName=ta['name'],time=showtime)
			allReviews = ArtistReview.objects.filter(artistId=artist_id)
			average = allReviews.aggregate(Avg('rating'))
			return render_to_response('artist.html', {'artist_pg': artist_pg, 'average': average, 'theUser': theUser, 'allReviews': allReviews, 'songData': songData, 'albumData': albumData})
	else:
		return render_to_response('artist.html', {'artist_pg': artist_pg, 'average': average, 'theUser': theUser, 'allReviews': allReviews, 'songData': songData, 'albumData': albumData})

def list_reviews(request):
	theUser = request.user
	songReview_pg = SongReview.objects.filter(user=theUser).order_by('-time')
	albumReview_pg = AlbumReview.objects.filter(user=theUser).order_by('-time')
	artistReview_pg = ArtistReview.objects.filter(user=theUser).order_by('-time')
	if not songReview_pg:
		songReview_pg = 'nope'
	if not albumReview_pg:
		albumReview_pg = 'nope'
	if not artistReview_pg:
		artistReview_pg = 'nope'
	return render_to_response('list_reviews.html',{'songReview_pg': songReview_pg, 'albumReview_pg': albumReview_pg, 'artistReview_pg': artistReview_pg})

def recommendations(request):
	token = credentials.get_access_token()
	sp = spotipy.Spotify(auth=token)
	Song.objects.all().delete()
	theRecommendedSongs = {}
	songs = []
	idList = []
	theUser = request.user
	songReviews = SongReview.objects.filter(user=theUser)
	if not songReviews:
		theRecommendedSongs = 'nonexistent'
	for r in songReviews:
		if r.rating > 6:
			songs.append(r.songId)
	if not songs:
		theRecommendedSongs = 'nonexistent'
	else:
		recommendedSongs = sp.recommendations(seed_artists=None,seed_genres=None,seed_tracks=songs,limit=40,country='US')
		for i in recommendedSongs['tracks']:
			idList.append(i['id'])
		for y in songReviews:
			if y.songId in idList:
				idList.remove(y.songId)
		recSongs = list(set(idList))
		for n in recSongs:
			theTrack = sp.track(n)
			songArtistLists = [x['name'] for x in theTrack['artists']]
			songArtists = ", ".join(songArtistLists)
			if not theTrack['album']['images']:
				theImage = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
			else:
				theImage = theTrack['album']['images'][0]['url']
			theSong = Song.objects.create(title=theTrack['name'],theType=theTrack['type'],albumId=theTrack['album']['id'],query='recs',album=theTrack['album']['name'],songId=theTrack['id'],preview=theTrack['preview_url'],external=theTrack['external_urls']['spotify'],uri=theTrack['uri'],duration='none',mainArtist=theTrack['artists'][0]['name'],artists=songArtists,popularity=theTrack['popularity'],image=theImage,artistId=theTrack['artists'][0]['id'])
			theRecommendedSongs = Song.objects.filter(query='recs')
	return render_to_response('recommendations.html',{'theRecommendedSongs': theRecommendedSongs})

def new_releases(request):
	token = credentials.get_access_token()
	sp = spotipy.Spotify(auth=token)
	Album.objects.all().delete()
	theNewStuff = sp.new_releases(country='US',limit=40)
	for i in theNewStuff['albums']['items']:
		theAlbum = sp.album(i['id'])
		albumArtistList = [x['name'] for x in theAlbum['artists']]
		albumArtists = ", ".join(albumArtistList)
		stringDate = unicodedata.normalize('NFKD', theAlbum['release_date']).encode('ascii','ignore')
		theYear = stringDate[:4]
		if not theAlbum['images']:
			theImage = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
		else:
			theImage = theAlbum['images'][0]['url']
		theAlbum = Album.objects.create(year=theYear,title=theAlbum['name'],theType=theAlbum['album_type'],popularity=float(theAlbum['popularity']),releaseDate=theAlbum['release_date'],query='reca',image=theAlbum['images'][0]['url'],albumId=theAlbum['id'],external=theAlbum['external_urls']['spotify'],uri=theAlbum['uri'],mainArtist=theAlbum['artists'][0]['name'],artists=albumArtists,artistId='nah')
		newAlbums = Album.objects.filter(query='reca')
	return render_to_response('new_releases.html',{'newAlbums': newAlbums})

def search_video(request):
	k = 'there is an error'
	if request.GET:
		videoSearch = request.GET.get('q')
		if 'r' in request.GET:
			results = youtube.search().list(q=videoSearch,part='snippet', type='video', maxResults=1).execute()
			for i in results['items']:
		 		k = unicodedata.normalize('NFKD', i['id']['videoId']).encode('ascii','ignore')
 			return render(request, 'searchvideo.html',{'vidData': k, 'searchVid': True})
 	else:
 		return render(request, 'searchvideo.html')

def search_lyrics(request):
	k = 'there is an error'
	if request.GET:
		lyricSearch = request.GET.get('q')
		if 'r' in request.GET:
			#try:
				lyricSearch = lyricSearch.encode('ascii','ignore')
				lyricSearch += ' song lyrics genius'
				name =  urllib.quote_plus(lyricSearch)
				url = 'http://www.google.com/search?q='+name
				result = requests.get(url).text
				link_start=result.find('genius.com')
				link_end=result.find('&',link_start)
				if link_start == -1 or link_end == -1:
					k = 'there is an error'
				else:
					link = 'https://' + result[link_start:link_end]
					lyrics_html = requests.get(link).text
					soup = BeautifulSoup(lyrics_html, "html.parser")
					[h.extract() for h in soup("script")]
					lyrics = soup.find("div", class_="lyrics").get_text()
					r = lyrics.encode('ascii','ignore')
					if not r:
						k = 'there is an error'
					else:
						k = r.split('\n')
			#except:
				#k = 'there is an error'
				return render(request, 'searchlyrics.html',{'lyricData': k, 'searchLyrics': True})
	else:
		return render(request,'searchlyrics.html')

 	
# def getVideo(song_name):
# 	results = youtube.search().list(q=song_name,part='snippet', type='video', maxResults=1).execute()
# 	for i in results['items']:
# 		k = unicodedata.normalize('NFKD', i['id']['videoId']).encode('ascii','ignore')
# 		return k


