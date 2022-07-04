from django.urls import path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index),
    path('search_media', views.search_media),
    path('play_track', views.play_track),
    # path('search_lyrics', views.search_lyrics),
    path('addNewTrack', views.addNewTrack),
    path('checkTracks', views.checkTracks),
    path('changeTracksOrder', views.changeTracksOrder),
    path('removeTrack', views.removeTrack),
    path('addNewPlaylist', views.addNewPlaylist),
    path('checkPlaylists', views.checkPlaylists),
    path('addNewSongToPlaylist', views.addNewSongToPlaylist),
    path('checkTracksInPlaylist', views.checkTracksInPlaylist),
    path('removePlaylist', views.removePlaylist)
]

urlpatterns += staticfiles_urlpatterns()