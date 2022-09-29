import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer


#deals with add button, opens file explorer and adds song to playlist
def find_song():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_song(filename_path)
    mixer.music.queue(filename_path)

#adds song to playlist
def add_song(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1

#deletes song from playlist
def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

#keeps time of the music
def keep_time(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            timeLabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1

#deals with play button, plays music
def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Music Player could not find the file. Please check again.')

#deals with stop button, stops music
def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"

#shows file details
def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    durationLabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target = keep_time, args = (total_length,))
    t1.start()

#deals with pause button, pauses music
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

#deals with rewind button, rewinds music
def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"

#sets the volume, set_volume only tkaes values between 0 and 1
def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

#deals with the mute button
def mute_music():
    global muted
    if muted:  #unmutes music
        mixer.music.set_volume(0.7)
        volumeButton.configure(image = volumeButtonImage)
        scale.set(70)
        muted = FALSE
    else:  #mutes music
        mixer.music.set_volume(0)
        volumeButton.configure(image = muteButtonImage)
        scale.set(0)
        muted = TRUE

#stops the program
def on_closing():
    stop_music()
    root.destroy()


# root which holds status bar, left and right frame
root = tk.ThemedTk()

#status bar that shows what is playing or if paused etc.
statusbar = ttk.Label(root, text = "Welcome to Melody", relief = SUNKEN, anchor = W, font = 'Times 10 italic')
statusbar.pack(side = BOTTOM, fill = X)

#contains the path and filename
playlist = []

# initialize the mixer
mixer.init()  

#title
root.title("Music Player")
root.iconbitmap('images/Music.ico')

#paused and muted global variables
paused = FALSE
muted = FALSE

#Frame that contains the playlist box, add and delete button
leftFrame = Frame(root)
leftFrame.pack(side = LEFT, padx = 30, pady = 30)

#playlist box
playlistbox = Listbox(leftFrame)
playlistbox.pack()

#Add button
addButton = ttk.Button(leftFrame, text = "+ Add", command = find_song)
addButton.pack(side = LEFT)

#Delete button
deleteButton = ttk.Button(leftFrame, text = "- Del", command = del_song)
deleteButton.pack(side = LEFT)

#Frame that takes up the right side of the menu
rightFrame = Frame(root)
rightFrame.pack(pady = 30)

#top right from
topRightFrame = Frame(rightFrame)
topRightFrame.pack()

#duration of song label
durationLabel = ttk.Label(topRightFrame, text = 'Total Duration : --:--')
durationLabel.pack(pady = 5)

#current time label
timeLabel = ttk.Label(topRightFrame, text = 'Current Time : --:--')
timeLabel.pack()

#middle right frame, contains play, stop, and pause button
midRightFrame = Frame(rightFrame)
midRightFrame.pack(pady = 30, padx = 30)

#Play Button
playPhoto = PhotoImage(file = 'images/play.png')
playBtn = ttk.Button(midRightFrame, image = playPhoto, command = play_music)
playBtn.grid(row = 0, column = 0, padx = 10)

#Stop Music Button
stopButtonImage = PhotoImage(file = 'images/stop.png')
stopButton = ttk.Button(midRightFrame, image = stopButtonImage, command = stop_music)
stopButton.grid(row = 0, column = 1, padx = 10)

#pause button
pauseButtonImage = PhotoImage(file = 'images/pause.png')
pauseButton = ttk.Button(midRightFrame, image = pauseButtonImage, command = pause_music)
pauseButton.grid(row = 0, column = 2, padx = 10)

# bottomRightFrame contains volume, rewind, and mute
bottomRightFrame = Frame(rightFrame)
bottomRightFrame.pack()

#rewind button
rewindButtonImage = PhotoImage(file = 'images/rewind.png')
rewindButtonButton = ttk.Button(bottomRightFrame, image = rewindButtonImage, command = rewind_music)
rewindButtonButton.grid(row = 0, column = 0)

#mute button
muteButtonImage = PhotoImage(file = 'images/mute.png')

#volume button
volumeButtonImage = PhotoImage(file = 'images/volume.png')
volumeButton = ttk.Button(bottomRightFrame, image = volumeButtonImage, command = mute_music)
volumeButton.grid(row = 0, column = 1)

#volume slider
scale = ttk.Scale(bottomRightFrame, from_ = 0, to = 100, orient = HORIZONTAL, command = set_vol)
scale.set(30)
mixer.music.set_volume(0.3)
scale.grid(row = 0, column = 2, pady = 15, padx = 30)

#closes amd stops the program
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()