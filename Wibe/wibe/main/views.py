from logging import exception
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import youtube_dl
from youtubesearchpython import VideosSearch
import requests
from bs4 import BeautifulSoup


def index(request):
    return render(request, 'main/index.html')

@csrf_exempt
def search_media(request):
    print("starting search media.")
    if request.method == 'POST': 

        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)
        # print(body) 	
        title = body['request']

        # print(title)


        videosSearch = VideosSearch(title, limit = 10)
        search_result = videosSearch.result()['result']
        # print(search_result[0])

        return JsonResponse({"status": 'Success', "response" : search_result})
    return JsonResponse({"status": 'Failed', "response" : "None"})          


@csrf_exempt
def play_track(request):
    if request.method == 'POST': 

            body_unicode = request.body.decode('utf-8') 	
            body = json.loads(body_unicode)
            # print(body) 	
            href = body['request']
            print(href)


            print("Trying to get audio...")

            ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
            with ydl:
                result = ydl.extract_info(
                    href,
                    download=False # We just want to extract the info and not download it
                )

            audio_source = result['formats'][1]['url']

            print("YT audio link is " + "\n" + audio_source)


            print("Audio sucessfully got.")

            return JsonResponse({"status" : 'Success', "sound" : audio_source})

# @csrf_exempt
# def search_lyrics(request):
#     if request.method == 'POST':
#         body_unicode = request.body.decode('utf-8') 	
#         body = json.loads(body_unicode)
#         # print(body) 	
#         title = body['request']
#         title = title.replace(" ", "+")
#         # print(title)

#         req = requests.get('https://search.azlyrics.com/search.php?q=' + title + "&x=28ee1736d269d551792144bcef2782050b77c4f0a5c78c0e558e92b826c02a50")
#         doc = BeautifulSoup(req.content, "lxml")
#         # print(doc)
#         links = doc.find_all("a")

#         # print(links)

#         # print(str(links[26]))
#         # print(str(links[27]))
#         song_link = str(links[28])
#         # print(str(links[29]))

    
#         semicolons = 0
#         x = 0
#         result = ""
#         for symbol in song_link:
#             if (symbol != '"'):
#                 if (semicolons == 1):
#                     result = result + symbol

#             if symbol == '"':
#                 semicolons = semicolons + 1

#             x = x + 1

#         print(result)

#         if result == "//www.azlyrics.com/add.php":
#             return JsonResponse({"status" : 'Success', "result" : "No results. Try enter song title above and check for response."})

#         else:
#             text_request = requests.get(result)
#             doc_lyrics = BeautifulSoup(text_request.content, "lxml")

#             text = str(doc_lyrics.find_all("div")[21])
#             # print(text)
            

#             return JsonResponse({"status" : 'Success', "result" : text})


@csrf_exempt
def addNewTrack(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)
        # print(body) 	
        title = body['track_title']
        link = body['yt_link']

        print(title)
        print(link)


        try:
            tracks_db = request.session['tracks']
            tracks_db.append({'title' : title, 'link' : link})
            request.session['tracks'] = tracks_db

        except:
            print('tracks_db is not exist yet.')
            request.session['tracks'] = [{'title' : title, 'link' : link}]

        print(request.session['tracks'])

        return JsonResponse({"status" : 'Success'})


def checkTracks(request):
    try:
        return JsonResponse({"status" : 'Success', "result" : request.session['tracks']})
    except:
        return JsonResponse({"status" : 'Failed', "result" : "Tracks base is not exist yet."})


@csrf_exempt
def changeTracksOrder(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)
        # print(body) 	
        sliced = slice(6, 10)
        first_song_id = int(body['first_song_id'][sliced])
        second_song_id = int(body['second_song_id'][sliced])
        first_song_title = body['first_song_title']
        second_song_title = body['second_song_title']
        first_song_link = body['first_song_link']
        second_song_link = body['second_song_link']

        tracks = request.session['tracks']
        


        tracks[first_song_id]['title'] = second_song_title
        tracks[first_song_id]['link'] = second_song_link
        tracks[second_song_id]['title'] = first_song_title
        tracks[second_song_id]['link'] = first_song_link

        request.session['tracks'] = tracks

        return JsonResponse({"status" : 'Success'})

@csrf_exempt
def removeTrack(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)
        # print(body) 	
        track_id = int(body['track_id'])

        tracks = request.session['tracks']

        track_info = tracks[track_id]

        print(track_info)

        try:
            pl_list = request.session['playlists']
            for pl in pl_list:
                x = 0
                for audio in pl['content']:
                    if (audio['link'] == track_info['link']):
                        pl['content'].pop(x)
                    x = x + 1
        except:
            print("Playlists base is not exist yet.")

        tracks.pop(track_id)

        request.session['tracks'] = tracks




        return JsonResponse({"status" : 'Success'})


@csrf_exempt
def addNewPlaylist(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)
        playlist_title = body['playlist_title']
        try:
            playlsits_db = request.session['playlists']
            playlsits_db.append({'playlist_title' : playlist_title, 'content' : []})
            request.session['playlists'] = playlsits_db

        except:
            print('playlsits_db is not exist yet.')
            request.session['playlists'] = [{'playlist_title' : playlist_title, 'content' : []}]


        return JsonResponse({"status" : 'Success'})

def checkPlaylists(request):
    try:
        return JsonResponse({'status' : 'Success', 'result' : request.session['playlists']})
    except:
        return JsonResponse({"status" : 'Failed', "result" : "Playlist base is not exist yet."})

@csrf_exempt
def addNewSongToPlaylist(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)
        title = body['title']
        link = body['link']
        playlist_title = body['playlist_title']

        print(title)
        print(link)
        print(playlist_title)
    
        
        try:
            pl_list = request.session['playlists']
            
            
            for pl in pl_list:
                print("перебор плейлистов.")
                if (pl['playlist_title'] == playlist_title):
                    print("найдено совпадение")
                    print(pl)
                    x = 0
                    for song in pl['content']:
                        print("перебор песен")
                        print(song)
                        if (song['link'] == link):
                            print("найдено совпадение по ссылке yt")
                            pl['content'].pop(x)
                            print("удалено")
                            print(pl)
                            request.session['playlists'] = pl_list
                            print("сессия установлена")
                            return JsonResponse({"status" : 'Success', "result" : "Song already exist in this playlist, removing it."})
                        x = x + 1
                    pl['content'].append({'title' : title, 'link' : link})
                    request.session['playlists'] = pl_list
                    break

                

            return JsonResponse({"status" : 'Success', "result" : "Added new song to playlist."})

        except:
            return JsonResponse({"status" : 'Failed', "result" : "Playlist base is not exist yet."})


@csrf_exempt
def checkTracksInPlaylist(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)

        try:
            pl_list = request.session['playlists']
            already_in_pl = []
            response = []
            for pl in pl_list:
                if (body['playlist_title'] == pl['playlist_title']):
                        try:
                            tracks_db = request.session['tracks']
                            for playlist_track in pl['content']:
                                for track in tracks_db:
                                    if (playlist_track['link'] == track['link']):
                                        already_in_pl.append(playlist_track['link'])



                                    
                            for track in tracks_db:
                                if track['link'] in already_in_pl:
                                    response.append({'title' : track['title'], 'link' : track['link'], 'include' : 'true'})
                                else:
                                    response.append({'title' : track['title'], 'link' : track['link'], 'include' : 'false'})

                            # print(response)

                            return JsonResponse({"status" : 'Success', "result" : response})

                        except:
                            return JsonResponse({"status" : 'Failed'})

        except:
            return JsonResponse({"status" : 'Failed', "result" : "Playlist base is not exist yet."})

@csrf_exempt
def removePlaylist(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)
        title = body['playlist_title']

        try:
            pl_list = request.session['playlists']
            # print(pl_list)
            x = 0
            for pl in pl_list:
                # print(pl)
                # print(x)
                if (pl['playlist_title'] == title):
                    pl_list.pop(x)
                    request.session['playlists'] = pl_list
                    return JsonResponse({"status" : 'Success', "result" : "Playlist removed."})
                x = x + 1
            return JsonResponse({"status" : 'Success', "result" : "Playlist not found."})
        except:
            return JsonResponse({"status" : 'Failed', "result" : "Playlist base is not exist yet."})
# removePlaylist