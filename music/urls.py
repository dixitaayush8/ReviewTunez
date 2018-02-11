from django.conf.urls import url, include
from django.contrib import admin
from music import views
from .views import search, song_page, album_page, artist_page, list_reviews, recommendations, new_releases, search_video
from .models import Song

urlpatterns = [
	url(r'^search/', search),
	url(r'^song/(?P<song_id>\w+)/$',song_page),
	url(r'^album/(?P<album_id>\w+)/$',album_page),
	url(r'^artist/(?P<artist_id>\w+)/$',artist_page),
	url(r'^list_reviews/', list_reviews),
	url(r'^recommendations/', recommendations),
	url(r'^new_releases/', new_releases),
	url(r'^searchvideo/', search_video)
]