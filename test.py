from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic
# a = YTMusic().get_mood_categories()

# print(a.keys())

# for i in a["Genres"]:
#     if(i["title"] == "Hindi"):
#         print(i)

# for i in a:
#     print(i)
# k = 1
# plt = {}
# for i in a:
#     for j in a[i]:
#         plt[k] = j
#         k+=1

# # print(plt)

# mI = int(input())
# if mI in plt:
#     opt = plt[mI]
#     b = YTMusic().get_mood_playlists(opt["params"])
#     print(b)
        


# b = YTMusic().get_mood_playlists("ggMPOg1uX2ZvbzNJMzJwRkFT")
# for i in b:
#     print(i["title"])

def generate_queue(self, current_video_id):
    "Fetch related songs and build a queue"
    self.queue = []
    related_songs = self.youtube_music.get_watch_playlist(current_video_id)["tracks"]

    if not related_songs:
        self.print("No related songs found!", "red")
        return

    for track in related_songs:
        self.queue.append((track["videoId"], track["title"]))

    self.queue_index = 0  # Start queue from first song
    self.print(f"🎶 Queue Updated! {len(self.queue)} songs added.", "cyan")

# c = YTMusic().get_playlist("RDCLAK5uy_mPolD_J22gS1SKxufARWcTZd1UrAH_0ZI")
# for i in c["tracks"]
#     print(i["videoId"])