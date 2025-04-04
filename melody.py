import os
import pygame
import threading
import cmd
from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic
import builtins
from termcolor import colored
import sys
import time

class MelodyCLI(cmd.Cmd):
    os.system("clear")
    intro = "Welcome to Melody CLI! Type 'help' to list commands."
    prompt = "(melody) "

    def __init__(self):
        super().__init__()
        self.youtube_music = YTMusic()
        self.currently_playing = None
        self.playback_thread = None
        self.is_paused = False
        self.manual_stop = False
        self.BASE_URL = 'https://www.youtube.com/watch?v='
        self.currSong = ""
        self.autoplay = True
        self.downloaded_tracks = []


    def print(self, text, color):
        builtins.print(colored(text, color))

    def do_clear(self, arg):
        os.system("clear")

    def do_autoplay(self, arg):
        "Toggle autoplay ON/OFF"
        self.autoplay = not self.autoplay
        status = "ON" if self.autoplay else "OFF"
        self.print(f"Autoplay is now {status} 🔁", "cyan")


    def do_search(self, searchString):
        "Search for a song: search <song name>"
        search_results = self.youtube_music.search(searchString)
        self.filtered_results = {}
        index = 1
        for result in search_results:
            if result["category"] in ["Songs", "Videos"]:
                self.filtered_results[index] = [result['videoId'], result['title']]
                self.print(f"{index}. {result['title']} - {result['duration']}", "yellow")
                index += 1

    def do_play(self, arg):
        try:
            song_id = self.filtered_results[int(arg)][0]
            self.currSong = self.filtered_results[int(arg)][1]
            mp3_file = self.downloadSong(song_id)
            if mp3_file:
                self.playSong(mp3_file)
                self.generate_queue(song_id)
        except Exception as e:
            self.print(f"Error: {e}", "red")
    
    def generate_queue(self, current_video_id):
        "Fetch related songs and build a queue"
        self.queue = []
        related_songs = self.youtube_music.get_watch_playlist(current_video_id)["tracks"]

        if not related_songs:
            self.print("No related songs found!", "red")
            return

        for track in related_songs:
            self.queue.append((track["videoId"], track["title"]))

        self.queue_index = 0
        self.print(f"🎶 Queue Updated! {len(self.queue)} songs added.", "cyan")

    def do_queue(self, arg):
        "Show the queue"
        idx = 1
        self.print("\n🎶 Queue", color="cyan")
        for songTuple in self.queue:
            self.print(f"{idx}. {songTuple[1]}", color="cyan")
            idx+=1

    def play_next(self):
        "Play the next song in the queue"
        if self.queue_index < len(self.queue) - 1:
            self.queue_index += 1
            next_song = self.queue[self.queue_index]
            self.currSong = next_song[1]
            self.print(f"⏭️ Now Playing: {self.currSong}", "green")
            self.playSong(self.downloadSong(next_song[0]))
        else:
            self.print("🎵 No more songs in queue! Fetching new songs...", "yellow")
            self.generate_queue(self.queue[self.queue_index][0])
            self.play_next()

    def do_next(self, arg):
        "Skip to the next song in queue"
        if self.queue_index < len(self.queue) - 1:
            self.play_next()
        else:
            self.print("🎵 Queue empty! Fetching new songs...", "yellow")
            self.generate_queue(self.queue[self.queue_index][0])  # Get new queue
            self.play_next()

    def do_prev(self, arg):
        "Play the previous song in queue"
        if self.queue_index > 0:
            self.queue_index -= 1
            prev_song = self.queue[self.queue_index]
            self.currSong = prev_song[1]
            self.print(f"⏮️ Replaying: {self.currSong}", "green")
            self.playSong(self.downloadSong(prev_song[0]))
        else:
            self.print("🚫 No previous songs!", "red")

    def do_pause(self, arg):
        "Pause the currently playing song"
        if pygame.mixer.music.get_busy() and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.print("Music paused ⏸️", "yellow")

    def do_resume(self, arg):
        "Resume a paused song"
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.print("Music resumed ▶️", "green")


    def do_stop(self, arg):
        "Stop the currently playing song and prevent autoplay"
        if self.currently_playing:
            self.manual_stop = True  # ✅ Set this before stopping
            pygame.mixer.music.stop()
            self.currently_playing = None
            self.is_paused = False
            self.clear_now_playing()
            self.print("Music stopped ⏹️", "yellow")


    def do_bye(self, arg):
        "Exit the application"
        self.print("Goodbye! 👋", "yellow")
        sys.exit(0)

    def downloadSong(self, videoID):
        "Check if song exists in cache, else download it."
        file_path = f"temp_audio/{videoID}.mp3"
        
        if os.path.exists(file_path):
            self.print(f"🎵 Using cached song: {file_path}", "green")
            return file_path

        url = f"{self.BASE_URL}{videoID}"
        os.makedirs("temp_audio", exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': file_path.replace(".mp3", ".%(ext)s"),
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=True)
                return file_path
        except Exception as e:
            self.print(f"❌ Error downloading: {e}", "red")
            return None

    def playSong(self, mp3_file):
        def _play():
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_file)
            pygame.mixer.music.play()
            self.is_paused = False
            self.manual_stop = False
            self.display_now_playing()

            while pygame.mixer.music.get_busy() or self.is_paused:
                time.sleep(1)

            if not self.manual_stop and self.autoplay and self.queue_index < len(self.queue) - 1:
                self.play_next()

            self.manual_stop = False 

        self.currently_playing = mp3_file
        self.playback_thread = threading.Thread(target=_play)
        self.playback_thread.start()


    def display_now_playing(self):
        print("\n" + "="*40)
        print(f"🎶 NOW PLAYING: {colored(self.currSong, 'cyan')}")
        print("="*40 + "\n")

    def clear_now_playing(self):
        print("\n" + " "*40, end="\r")
        print("\n" + "="*40)
        print("🎵 No song is currently playing.")
        print("="*40 + "\n")


if __name__ == "__main__":
    MelodyCLI().cmdloop()
