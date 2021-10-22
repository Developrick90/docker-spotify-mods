import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import time

# file locations
file_time_playing = "time_playing.txt"
file_time_playing_ms = "time_playing_ms.txt"
file_time_total = "time_total.txt"
file_time_total_ms = "time_total_ms.txt"
artist_cutoff = 25
song_cutoff = 28
cutoff_txt = "..."

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="...",
                                               client_secret="...",
                                               redirect_uri="http://localhost:8080",
                                               scope="user-read-playback-state"))


def play_time():
    global time_playing
    try:
        millis = int(currently_playing["progress_ms"])
        seconds = (format(int((millis / 1000) % 60), '02'))
        minutes = int((millis / (1000 * 60)) % 60)

        time_playing = str(minutes) + ":" + seconds

        with open(file_time_playing, "w", encoding="utf-8") as f:
            f.write(str(time_playing))
        with open(file_time_playing_ms, "w", encoding="utf-8") as f:
            f.write(str(millis))
    except:
        pass


def total_time():
    global time_total
    try:
        millis = int(currently_playing["item"]["duration_ms"])
        seconds = (format(int((millis / 1000) % 60), '02'))
        minutes = int((millis / (1000 * 60)) % 60)

        time_total = str(minutes) + ":" + seconds

        with open(file_time_total, "w", encoding="utf-8") as f:
            f.write(str(time_total))

        with open(file_time_total_ms, "w", encoding="utf-8") as f:
            f.write(str(millis))
    except:
        pass
    play_time()


def artists():
    try:
        with open("artist.txt", "w", encoding="utf-8") as f:
            i = currently_playing["item"]["artists"]

            playing_artist = []
            while 1 == 1:
                start = (str(i).find("'name': '")) + 9

                if start == 8:
                    break

                end = (str(i)[start:].find("', '"))
                i = str(i)[start:]
                playing_artist.append(i[:end])
                artist = str(playing_artist).replace("'", "")

            artist = artist[1:-1]
            if len(artist) > artist_cutoff:
                artist = artist[:artist_cutoff - len(cutoff_txt)]
                if artist[-1:] == " ":
                    artist = artist[:-1] + cutoff_txt
                else:
                    artist = artist + cutoff_txt
            f.write(artist)
    except:
        pass


def album():
    try:
        with open("cover.jpg", "wb") as f:
            img_data = requests.get(currently_playing["item"]['album']['images'][0]['url']).content
            f.write(img_data)
    except:
        pass


def bad_words():
    try:
        test = currently_playing["item"]["explicit"]
        if str(test) == "True":
            sp.next_track()
    except:
        pass


def track():
    global song
    global currently_playing
    try:
        currently_playing = sp.currently_playing()

        if song == str(currently_playing["item"]["name"]):
            play_time()
            return

        else:
            song = str(currently_playing["item"]["name"])

            with open("song.txt", "w", encoding="utf-8") as f:
                if len(song) > song_cutoff:
                    song = song[:song_cutoff - len(cutoff_txt)]
                    if song[-1:] == " ":
                        song = song[:-1] + cutoff_txt
                    else:
                        song = song + cutoff_txt
                f.write(song)
                song = str(currently_playing["item"]["name"])

            artists()
            album()
            total_time()
    except:
        pass

song = ""
starttime = time.time()
while True:
    track()
    time.sleep(0.5 - ((time.time() - starttime) % 0.5))
