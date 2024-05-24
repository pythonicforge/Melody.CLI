import os
import pygame
import threading
import time
from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic

class Player():
    def __init__(self) -> None:
        """
        Initialize the Player class.

        Attributes:
        -----------
        youtube_music : YTMusic
            An instance of YTMusic class for interacting with YouTube Music.
        index : int
            A counter to keep track of the search results.
        filtered_results : dict
            A dictionary to store the filtered search results.
        currently_playing : str
            The currently playing song's file path.
        playback_thread : threading.Thread
            A thread for playing the song.
        is_paused : bool
            A flag to indicate whether the song is paused.
        BASE_URL : str
            The base URL for YouTube video links.
        """
        self.youtube_music = YTMusic()
        self.index = 1
        self.filtered_results = {}
        self.currently_playing = None
        self.playback_thread = None
        self.is_paused = False
        self.BASE_URL = 'https://www.youtube.com/watch?v='
        
    def searchSong(self, searchString):
        """
        Searches for a song on YouTube Music using the provided search string.

        Parameters:
        searchString (str): The search string to be used for searching the song.

        Returns:
        dict, dict: A dictionary containing the search results and another dictionary containing the filtered search results.

        Raises:
        Exception: If the search results are empty.

        Example:
        >>> player = Player()
        >>> search_results, filtered_results = player.searchSong("song title")
        """
        searches = {}
        search_results = self.youtube_music.search(searchString)
        for search in search_results:
            if(search["category"] == 'Songs' or search["category"] == "Videos"):
                self.filtered_results[self.index] = search['videoId']
                searches["Title"] = search['title']
                searches["Type"] = search['resultType']
                searches["Duration"] = search['duration']
                searches["Video-ID"] = search['videoId']
                searches["Artists"] = search['artists']
                self.index += 1
            
        return searches, self.filtered_results
    
    def downloadSong(self, videoID):
        """
        Downloads the audio file of the specified YouTube video.

        Parameters:
        videoID (str): The unique identifier of the YouTube video.

        Returns:
        str: The path to the downloaded audio file.

        Raises:
        Exception: If an error occurs during the download or conversion process.

        Example:
        >>> player = Player()
        >>> audio_file = player.downloadSong("video_id")
        """
        url = f"{self.BASE_URL}{str(videoID)}"
        os.makedirs("temp_audio", exist_ok=True)
        t = time.time()
        ml = int(t * 1000)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'temp_audio/Audio_{videoID + str(t)}.%(ext)s',
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
                ydl.download([url])
                audio_file = f'temp_audio/Audio_{videoID + str(t)}.mp3'
                print(f"Download and conversion complete: {audio_file}")
                return audio_file
        except Exception as e:
            print(f"Error: {e}")
            return None

    def playSong(self, mp3_file):
        """
        Plays the specified audio file using the Pygame library.

        Parameters:
        mp3_file (str): The path to the audio file to be played.

        Returns:
        None

        Raises:
        Exception: If an error occurs during the playback process.

        Example:
        >>> player = Player()
        >>> player.playSong("path_to_audio_file.mp3")
        """
        def _play():
            """
            Internal function to initialize Pygame, load the audio file, and start playback.

            Parameters:
            None

            Returns:
            None

            Raises:
            Exception: If an error occurs during the playback process.
            """
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() or self.is_paused:
                pygame.time.Clock().tick(10)
            self.stopSong()

        self.currently_playing = mp3_file
        self.playback_thread = threading.Thread(target=_play)
        self.playback_thread.start()

    def pauseSong(self):
        """
        Pauses the currently playing song if it is not already paused.

        Parameters:
        None

        Returns:
        None

        Raises:
        Exception: If there is no currently playing song.

        Example:
        >>> player = Player()
        >>> player.playSong("path_to_audio_file.mp3")
        >>> player.pauseSong()
        """
        if self.currently_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            print("Music paused")

    def resumeSong(self):
        """
        Resumes the currently playing song if it is paused.

        Parameters:
        None

        Returns:
        None

        Raises:
        Exception: If there is no currently playing song.

        Example:
        >>> player = Player()
        >>> player.playSong("path_to_audio_file.mp3")
        >>> player.pauseSong()
        >>> player.resumeSong()
        """
        if self.currently_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            print("Music resumed")

    def stopSong(self):
        """
        Stops the currently playing song and resets the player's state.

        Parameters:
        None

        Returns:
        None

        Raises:
        Exception: If there is no currently playing song.

        Example:
        >>> player = Player()
        >>> player.playSong("path_to_audio_file.mp3")
        >>> player.stopSong()
        """
        if self.currently_playing:
            pygame.mixer.music.stop()
            self.currently_playing = None
            self.is_paused = False
