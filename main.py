from Melody_CLI import Player

player = Player()
searchQuery = input("Search for a song: ")
youtubeSearchResults, videoIDS = player.searchSong(searchQuery)
desiredVideo = int(input("Enter desired video number: "))
audioFile = player.downloadSong(videoIDS[desiredVideo])
player.playSong(audioFile)
