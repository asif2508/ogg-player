from tkinter import *
import os
from tkinter import filedialog
from tkinter import messagebox
import pygame
from tkinter import ttk
from mutagen.oggvorbis import OggVorbis
import time
root = Tk()
root.title("OGG PLAYER")
root.geometry("530x380")
pygame.mixer.init()
##Functions
##PLAYTIME FUNCTIONS
def playtime():
    if stopped == True:
        song_slider.config(value=0)
        return
    current_position = pygame.mixer.music.get_pos()/1000
    converted_time = time.strftime("%H:%M:%S", time.gmtime(current_position))
    #getting active song name and value
    song = musiclist_box.get(ACTIVE)
    song =f"{dirpath}{song}.ogg"
    #getting song length
    song_mut = OggVorbis(song)
    song_length = song_mut.info.length
    converted_song_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
    song_slider_frame.config(text=converted_song_length)
    #moving slider position
    if int(song_slider.get()) == int(song_length):
        stop()
    elif paused == True:
        pass
    else:
        next_time = (song_slider.get()) + 1
        song_slider.config(to=song_length, value=next_time)
        converted_time = time.strftime("%H:%M:%S", time.gmtime(int(song_slider.get())))
    if current_position > 0:
        song_label.config(text=f"Time elapsed: {converted_time}")
    song_label.after(1000, playtime)
    
#adding one song functions
def add_one_song():
    global dirpath
    song = filedialog.askopenfilename(initialdir="/home/asif/python3/mp3player/songs/", title="open a song", filetypes=(("OGG files", "*.ogg"),))
    dirpath = os.path.dirname(song)+"/"
    song = song.replace(dirpath, "")
    song = song.replace(".ogg", "")
    musiclist_box.insert(END, song)

#adding many songs
def add_many_songs():
    global dirpath
    songs = filedialog.askopenfilenames(initialdir="/home/asif/python3/mp3player/songs/",title="open a song", filetypes=(("OGG files", "*.ogg"),))
    for paths in songs:
        dirpath = os.path.dirname(paths)
        break
    
    dirpath = dirpath + "/"
    for song in songs:
        song = song.replace(dirpath, "")
        song = song.replace(".ogg", "")
        musiclist_box.insert(END, song)
#remove one song func
def remove_one_song():
    musiclist_box.delete(ANCHOR)
#removing all songs
def remove_all_songs():
    musiclist_box.delete(0, END)

#about function
def about():
    messagebox.showinfo("About", "OGG Player developed by Rakibul Hasan Asif")
##SONG CONTROLLING function
#play function
def play():
    #setting stopped to false to retrun a new value
    global stopped
    stopped = False
    song_slider.config(value=0)
    #selected song
    song = musiclist_box.get(ACTIVE)
    #adding dirpath
    song = f"{dirpath}{song}.ogg"
    #adding song name in status bar
    song_a = song.replace(dirpath, "")
    song_a = song_a.replace("/", "")
    my_label.config(text=f"Playing: {song_a}")
    #loading to pygame
    pygame.mixer.music.load(song)
    #playing the song
    pygame.mixer.music.play(loops=0)
    playtime()
global stopped
stopped= False
#stop functions
def stop():
    pygame.mixer.music.stop()
    musiclist_box.selection_clear(ACTIVE)
    my_label.config(text="")
    song_label.config(text="Time elapsed: 00:00:00")
    song_slider_frame.config(text="00:00:00")
    global stopped
    stopped = True
#pause function
global paused
paused = False
def pause(x):
    global paused
    paused = x
    if paused == True:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True
#forward function
def forward():
    #setting the song slider
    song_slider.config(value=0)
    next_song = musiclist_box.curselection()
    next_song = next_song[0] + 1
    song = musiclist_box.get(next_song)
    song = f"{dirpath}/{song}.ogg"
    song_a = song.replace(dirpath, "")
    song_a = song_a.replace("/", "")
    my_label.config(text=f"Playing: {song_a}")
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    #selecting the music
    musiclist_box.selection_clear(0, END)
    musiclist_box.activate(next_song)
    musiclist_box.selection_set(next_song, last=None)
#back functions
def back():
    #settng up the slider
    song_slider.config(value=0)
    pre_song = musiclist_box.curselection()
    pre_song = pre_song[0] - 1
    song = musiclist_box.get(pre_song)
    song = f"{dirpath}/{song}.ogg"
    song_a = song.replace(dirpath, "")
    song_a = song_a.replace("/", "")
    my_label.config(text=f"Playing: {song_a}")
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    #settng up the music playlist
    musiclist_box.selection_clear(0, END)
    musiclist_box.activate(pre_song)
    musiclist_box.selection_set(pre_song)
##ADDING VOLUME
def volume(x):
    pygame.mixer.music.set_volume(v_slider.get())
    global v_value
    v_value = int(v_slider.get()*100)
    v_label.config(text=v_value)
def slider(x):
    song = musiclist_box.get(ACTIVE)
    song = f"{dirpath}{song}.ogg"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=song_slider.get())
#adding mainframe
main_frame = Frame(root, bg="crimson")
main_frame.pack(fill="both", expand=1)

#ADDING MUSIC LIST BOX
musiclist_box = Listbox(main_frame, width=42, bg="hotpink", fg="white", selectbackground="slateblue", selectforeground="white", font=("roboto"))
musiclist_box.grid(row=0, column=0, padx=10, pady=10)
#SONG SLIDER
song_slider_frame = LabelFrame(main_frame, text="00:00:00", font=("roboto"),bg="maroon", relief="raised")
song_slider_frame.grid(row=1, column=0, columnspan=5, sticky=W, padx=10)
song_slider = ttk.Scale(song_slider_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=417, command=slider)
song_slider.pack()
song_label = Label(song_slider_frame, text="Time elapsed: 00:00:00", font=("roboto"),bg="maroon" )
song_label.pack()
#ADDING MAIN OPTIONS MENU BAR FRAME
options_frame = Frame(main_frame, bg="maroon", relief="raised")
options_frame.grid(row=2, column=0)

#ADDING BUTTON IMAGE
play_btn_img = PhotoImage(file="/home/asif/Documents/python3/GUI/CODEMY/mp3player/images/play50.png")
forward_btn_img = PhotoImage(file="/home/asif/Documents/python3/GUI/CODEMY/mp3player/images/forward50.png")
back_btn_img = PhotoImage(file="/home/asif/Documents/python3/GUI/CODEMY/mp3player/images/back50.png")
pause_btn_img = PhotoImage(file="/home/asif/Documents/python3/GUI/CODEMY/mp3player/images/pause50.png")
stop_btn_img = PhotoImage(file="/home/asif/Documents/python3/GUI/CODEMY/mp3player/images/stop50.png")
#ADDING MAIN BUTTON
play_button = Button(options_frame, image=play_btn_img, borderwidth=1, bg="maroon",command=play)
pause_button = Button(options_frame, image=pause_btn_img, borderwidth=1, bg="maroon", command=lambda: pause(paused))
back_button = Button(options_frame, image=back_btn_img, borderwidth=1, bg="maroon", command=back)
forward_button = Button(options_frame, image=forward_btn_img, borderwidth=1, bg="maroon", command=forward)
stop_button = Button(options_frame,image=stop_btn_img, borderwidth=1, bg="maroon", command=stop)
back_button.grid(row=1, column=0, padx=5, pady=3)
forward_button.grid(row=1, column=1, padx=5,pady=3)
play_button.grid(row=1, column=2, padx=5, pady=3)
pause_button.grid(row=1, column=3, padx=5, pady=3)
stop_button.grid(row=1, column=4, padx=5, pady=3)

#ADDING MAIN MENU
my_menu = Menu(root, background='darkred', foreground='white',
               activebackground='darkorange', activeforeground='cornsilk', font=("roboto"), bd=1, relief="raised")
root.config(menu=my_menu)
#ADDING ADD SONG SUB MENU
add_songs = Menu(my_menu, background='lightblue', foreground='black',
               activebackground='#004c99', activeforeground='white', bd=2,font=("roboto"), tearoff=0)
my_menu.add_cascade(label="Add songs", menu=add_songs)
add_songs.add_command(label="Add one song", command=add_one_song)
add_songs.add_command(label="Add many songs", command=add_many_songs)

#ADDING remove SONG SUB MENU
rmv_songs = Menu(my_menu, background='lightblue', foreground='black',
               activebackground='#004c99', activeforeground='white', bd=2,font=("roboto"), tearoff=0)
my_menu.add_cascade(label="Remove songs", menu=rmv_songs)
rmv_songs.add_command(label="Remove one song", command=remove_one_song)
rmv_songs.add_command(label="Remove all songs", command=remove_all_songs)

options_menu = Menu(my_menu, background='lightblue', foreground='black',
               activebackground='#004c99', activeforeground='white', bd=2,font=("roboto"), tearoff=0)
my_menu.add_cascade(label="More options", menu=options_menu)
options_menu.add_command(label="About", command=about)
options_menu.add_command(label="Exit", command=root.quit)
#volume gui
volume_label_frame = LabelFrame(main_frame,text="volume", font=("roboto"), bg="crimson", relief="raised")
volume_label_frame.grid(row=0, column=1)
v_slider = ttk.Scale(volume_label_frame, from_=1, to=0, orient=VERTICAL, value=.50, length=161, command=volume)
v_slider.pack()

v_label = Label(volume_label_frame, text=int(v_slider.get()*100), font=("roboto"),bg="crimson", fg="white")
v_label.pack()


#STATUS BAR
my_label = Label(root, text="", bd=1, relief="raised", anchor=W, bg="darkred")
my_label.pack(fill=X, side=BOTTOM, ipady=1)











root.mainloop()