#!/usr/bin/env python3

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

from typing import Optional, Literal

class MelodyCLI(cmd.Cmd):
    os.system("clear")
    intro = "Welcome to Melody.CLI! Type 'help' to list commands."
    prompt = "(melody) "

    def __init__(self):
        super().__init__()
        self.youtube_music = YTMusic()
        self.BASE_URL = 'https://www.youtube.com/watch?v='
        self.queue: list[tuple[str, str]] = []
        self.currSong: str = ""
        self.queue_index: int = 0
        self.autoplay: bool = True
        self.is_paused: bool = False
        self.playback_thread: threading.Thread | None = None
        self.currently_playing: str | None = None
        self.filtered_results:  dict[int, list[str]] = {}

    def print(self, text:str, color:Optional[Literal['black', 'grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'light_grey', 'dark_grey', 'light_red', 'light_green', 'light_yellow', 'light_blue', 'light_magenta', 'light_cyan', 'white']]) -> None:
        """Modified print function that prints text with colors"""
        builtins.print(colored(text, color))

    def do_clear(self, arg:str) -> None:
        """Clears the terminal screen"""
        os.system("clear")

    def do_search(self, searchString:str) -> None:
        "Search for a song: search <song name>"
        if not searchString.strip():
            self.print("Please provide a search query!", "red")
            return

        search_results = self.youtube_music.search(searchString)
        self.filtered_results = {}
        index = 1
        for result in search_results:
            if result.get("category") in ["Songs", "Videos"] and "videoId" in result:
                self.filtered_results[index] = [result['videoId'], result['title']]
                self.print(f"{index}. {result['title']} - {result.get('duration', 'Unknown Duration')}", "yellow")
                index += 1

    def do_play(self, arg:str) -> None:
        try:
            index = int(arg)
            song_id = self.filtered_results[index][0]
            self.currSong = self.filtered_results[index][1]
            mp3_file = self.downloadSong(song_id)
            if mp3_file:
                self.playSong(mp3_file)
                self.generate_queue(song_id)
        except (KeyError, ValueError):
            self.print("Invalid index or no search results available.", "red")
        except Exception as e:
            self.print(f"Error: {e}", "red")

    def do_next(self, arg:str) -> None:
        self.play_next()

    def play_next(self) -> None:
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

    def do_prev(self, arg:str) -> None:
        if self.queue_index > 0:
            self.queue_index -= 1
            prev_song = self.queue[self.queue_index]
            self.currSong = prev_song[1]
            self.print(f"⏮️ Replaying: {self.currSong}", "green")
            self.playSong(self.downloadSong(prev_song[0]))
        else:
            self.print("🚫 No previous songs!", "red")

    def do_pause(self, arg:str) -> None:
        if pygame.mixer.music.get_busy() and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.print("Music paused ⏸️", "yellow")

    def do_resume(self, arg:str) -> None:
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.print("Music resumed ▶️", "green")

    def do_bye(self, arg:str) -> None:
        self.print("Shutting down Melody CLI... 👋", "yellow")
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                pygame.quit()
                self.print("Audio system closed 🔇", "magenta")
        except Exception as e:
            self.print(f"Error stopping audio: {e}", "red")
        
        if self.playback_thread and self.playback_thread.is_alive():
            self.print("Waiting for playback thread to close... ⏳", "yellow")
            self.playback_thread.join(timeout=2)

        self.print("Goodbye! 👋", "green")
        sys.exit(0)

    def do_autoplay(self, arg:str) -> None:
        "Toggle autoplay ON/OFF"
        self.autoplay = not self.autoplay
        status = "ON" if self.autoplay else "OFF"
        self.print(f"Autoplay is now {status} 🔁", "cyan")

    def generate_queue(self, current_video_id:str) -> None:
        "Fetch related songs and build a queue"
        self.queue = []
        self.queue_index = 0
        try:
            related_songs = self.youtube_music.get_watch_playlist(current_video_id).get("tracks", [])
            if not related_songs:
                self.print("No related songs found!", "red")
                return
            for track in related_songs:
                self.queue.append((track["videoId"], track["title"]))
            self.print(f"🎶 Queue Updated! {len(self.queue)} songs added.", "cyan")
        except Exception as e:
            self.print(f"Error fetching related songs: {e}", "red")

    def do_queue(self, arg:str) -> None:
        "Show the queue"
        self.print("\n🎶 Queue", color="cyan")
        for idx, songTuple in enumerate(self.queue, start=1):
            self.print(f"{idx}. {songTuple[1]}", color="cyan")

    def do_queueplay(self, arg:str) -> None:
        "Play a specific song from the queue: queueplay <index>"
        try:
            index = int(arg) - 1
            if 0 <= index < len(self.queue):
                self.queue_index = index
                song_id, title = self.queue[self.queue_index]
                self.currSong = title
                self.print(f"🎵 Playing from queue: {title}", "green")
                mp3_file = self.downloadSong(song_id)
                if mp3_file:
                    self.playSong(mp3_file)
                else:
                    self.print("⚠️ Failed to play song.", "red")
            else:
                self.print("❌ Index out of range!", "red")
        except ValueError:
            self.print("❌ Please enter a valid number. Usage: queueplay <index>", "red")
        except Exception as e:
            self.print(f"⚠️ Error playing from queue: {e}", "red")

    def do_clearqueue(self,current_video_id:str) -> None:
        "Clear the queue"
        self.queue = []
        self.queue_index = 0
        self.print("🧹 Queue has been cleared", "green")

    def downloadSong(self, videoID: str) -> str:
        file_path = f"temp_audio/{videoID}.opus"

        if os.path.exists(file_path):
            self.print(f"🎵 Using cached song: {file_path}", "green")
            return file_path

        url = f"{self.BASE_URL}{videoID}"
        os.makedirs("temp_audio", exist_ok=True)

        ydl_opts = {
            'format': 'ba', # ba = best audio, typically webm container with opus audio
            'outtmpl': file_path.replace(".opus", ".%(ext)s"),
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
            }],
            'http_headers': {  # Add HTTP headers
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            },
        }

        try:
            self.print(f"⬇️ Downloading: {url}", "yellow")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=True)
            self.print(f"🎵 Downloaded track: {file_path}", "green")
            return file_path
        except Exception as e:
            self.print(f"❌ Error downloading: {e}", "red")
            return None

    def playSong(self, audio_file:str) -> None:
        def _play():
            try:
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                self.is_paused = False
                self.display_now_playing()

                while pygame.mixer.music.get_busy() or self.is_paused:
                    time.sleep(1)

                if self.autoplay and self.queue_index < len(self.queue) - 1:
                    self.play_next()
            except Exception as e:
                self.print(f"Playback error: {e}", "red")

        self.currently_playing = audio_file
        self.playback_thread = threading.Thread(target=_play)
        self.playback_thread.start()

    def display_now_playing(self) -> None:
        print("\n" + "="*40)
        print(f"🎶 NOW PLAYING: {colored(self.currSong, 'cyan')}")
        print("="*40 + "\n")

    def clear_now_playing(self) -> None:
        print("\n" + "="*40)
        print("🎵 No song is currently playing.")
        print("="*40 + "\n")

if __name__ == "__main__":
    try:
        MelodyCLI().cmdloop()
    except KeyboardInterrupt:
        print("\n💥 Keyboard Interrupt! Shutting down Melody CLI...")
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()
        sys.exit(0)
