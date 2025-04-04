# _🎵 Melody CLI_

![banner](https://github.com/pythonicforge/Melody.CLI/blob/main/assets/banner.png)

### _Terminal Tunes, Done Right._

**Melody CLI** is a powerful, minimal, and interactive command-line music player that lets you search, download, and play songs from YouTube Music – all inside your terminal.

Built with Python, powered by `ytmusicapi`, `yt-dlp`, and `pygame`, this tool gives devs and terminal geeks a lightweight, distraction-free music experience.

### 🚀 Features

- 🔍 **Search Songs** from YouTube Music right inside the terminal  
- ⬇️ **Download & Cache Audio** using `yt-dlp` for efficient playback  
- 🎧 **Play Music** with smooth `pygame` integration  
- ⏸️ **Playback Controls** – Pause, Resume, Stop, Skip, Previous  
- 🔁 **Autoplay Queue** – Auto-queues and plays recommended tracks  
- 🧠 **Smart Caching** – Replays already downloaded tracks to save bandwidth  
- 🧹 **Disk Management** – Only keeps the last 10 played songs in cache  
- 🧼 **Clear CLI** – Use `clear` to reset your screen mid-session  


### 🛠️ Setup & Usage

#### 🔄 Clone the Project

```bash
git clone https://github.com/pythonicforge/Melody.CLI
cd Melody.CLI
```

#### 📦 Set Up Environment

```bash
python3 -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
pip install -r requirements.txt
```


### 🎮 Run Melody CLI

```bash
python melody.py
```

Once you're in the CLI, use commands like:

```bash
search <song name>   # Search songs
play <index>         # Play a song from search results
pause                # Pause music
resume               # Resume playback
stop                 # Stop playback (also disables autoplay)
next                 # Play next song in the queue
prev                 # Play previous song
queue                # View the current queue
autoplay             # Toggle autoplay on/off
clear                # Clear the terminal screen
bye                  # Exit the CLI
```


### 🧠 How It Works

- **Search:** Uses `ytmusicapi` to find relevant tracks.
- **Download:** Fetches audio from YouTube with `yt-dlp`, stores it as MP3.
- **Playback:** Uses `pygame` for low-latency audio control.
- **Queue:** Automatically fills up with related tracks post-playback.
- **Memory Friendly:** Automatically keeps cache folder to a max of 10 songs.


### 💡 Tech Stack

| Purpose          | Tool           |
|------------------|----------------|
| Search API       | ytmusicapi     |
| Download Engine  | yt-dlp         |
| Audio Playback   | pygame         |
| CLI Framework    | Python's `cmd` |


### 🤝 Contribute

Got ideas? Found bugs?  
Pull requests and issues are super welcome! Let’s make terminal music cool again 💻🎶


### 📢 Final Note

This isn’t your average MP3 player – **Melody CLI** is for the terminal generation. It’s fast, snappy, and doesn’t need a GUI to vibe.

