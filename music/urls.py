from django.conf.urls import url, include
from django.contrib import admin
from music import views
from .views import search, song_page
from .models import Song

urlpatterns = [
	url(r'^search/', search),
	url(r'^song/(?P<song_id>\w+)/$',song_page),
]