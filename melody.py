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
        self.BASE_URL = 'https://www.youtube.com/watch?v='
        self.currSong = ""

    def print(self, text, color):
        builtins.print(colored(text, color))

    def do_clear(self, arg):
        os.system("clear")

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
        except Exception as e:
            self.print(f"Error: {e}", "red")

    def do_pause(self, arg):
        "Pause the currently playing song"
        if self.currently_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.print("Music paused ⏸️", "yellow")

    def do_resume(self, arg):
        "Resume a paused song"
        if self.currently_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.print("Music resumed ▶️", "green")

    def do_stop(self, arg):
        "Stop the currently playing song"
        if self.currently_playing:
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
        url = f"{self.BASE_URL}{videoID}"
        os.makedirs("temp_audio", exist_ok=True)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'temp_audio/{videoID}.%(ext)s',
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
                info = ydl.extract_info(url, download=True)
                return f'temp_audio/{videoID}.mp3'
        except Exception as e:
            self.print(f"Error: {e}", "red")
            return None

    def playSong(self, mp3_file):
        def _play():
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_file)
            pygame.mixer.music.play()
            self.display_now_playing()
            while pygame.mixer.music.get_busy() or self.is_paused:
                time.sleep(1)
            self.do_stop(None)

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
