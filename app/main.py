import os
import pygame
from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic

class Player():
    def __init__(self) -> None:
        """
        Initialize the Player class.

        Parameters:
        None

        Returns:
        None

        Attributes:
        self.youtube_music: An instance of YTMusic class for interacting with YouTube Music.
        self.index: An integer representing the current index for displaying search results.
        self.filtered_results: A dictionary to store the filtered search results.
        self.BASE_URL: A string representing the base URL for YouTube video links.
        """
        self.youtube_music = YTMusic()
        self.index = 1
        self.filtered_results = {}
        self.BASE_URL = 'https://www.youtube.com/watch?v='
        
    def searchSong(self, searchString):
        """
        Search for a song on YouTube Music and return the downloadable audio file.

        Parameters:
        searchString (str): The search query for the song.

        Returns:
        str: The path to the downloaded audio file.

        Raises:
        Exception: If an error occurs during the download or conversion process.

        Attributes:
        self.youtube_music: An instance of YTMusic class for interacting with YouTube Music.
        self.index: An integer representing the current index for displaying search results.
        self.filtered_results: A dictionary to store the filtered search results.
        self.BASE_URL: A string representing the base URL for YouTube video links.
        """
        search_results = self.youtube_music.search(searchString)
        for search in search_results:
            if(search["category"] == 'Songs' or search["category"] == "Videos"):
                print(f"{self.index}.", end=" ")
                self.filtered_results[self.index] = search['videoId']
                print(f"Title: {search['title']}\n   Type: {search['resultType']}\n   Duration: {search['duration']}\n   Video-ID: {search['videoId']}\n   Artists: {search['artists']}\n")
                self.index += 1
                
        choice = int(input("Enter the number of your choice of song: "))
        url = f"{self.BASE_URL}{self.filtered_results[choice]}"
        
        os.makedirs("temp_audio", exist_ok=True)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'temp_audio/{self.filtered_results[choice]}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                audio_file = f'temp_audio/{self.filtered_results[choice]}.mp3'
                print("Download and conversion complete:", audio_file)
                return audio_file
        except Exception as e:
            print(f"Error: {e}")
            return None

    def playSong(self, mp3_file):
        """
        Plays the specified mp3 file using Pygame.

        Parameters:
        mp3_file (str): The path to the mp3 file to be played.

        Returns:
        None.

        Raises:
        Exception: If an error occurs during the playback or deletion of the file.

        Attributes:
        self.pygame: An instance of the Pygame library for audio playback.
        self.mp3_file: The path to the mp3 file to be played.

        Notes:
        - The function initializes Pygame and loads the specified mp3 file.
        - It then attempts to play the file using Pygame's mixer module.
        - If the file is successfully played, it is stopped and deleted after playback.
        - If an error occurs during playback or deletion, an Exception is raised.
        """
        if mp3_file:
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_file)
            try:
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except Exception as e:
                print(e)
            finally:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                try:
                    os.remove(mp3_file)
                    print(f"Deleted file: {mp3_file}")
                except Exception as e:
                    print(f"Error deleting file: {e}")
        else:
            print("No file to play")

if __name__ == '__main__':
    player = Player()
    mp3_file = player.searchSong(input("Search for a song: "))
    player.playSong(mp3_file=mp3_file)
