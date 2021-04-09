import robot as song_robot
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from threading import Thread
from time import sleep

error_song = 0
total_finished_song = 0
finished_song = 0
row_count=2
song_dict = {} # contains remove btns
new_song_label_dict = {}
window = tk.Tk()
window.title("Simple Text Editor")
song_count = 0
download=False
frame_main = tk.Frame(window, bg="gray")
frame_right = tk.Frame(window, bg="yellow")
frame_main.grid(sticky='news')
frame_right.grid(sticky='news')

# Create a frame for the canvas with non-zero row&column weights
frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)

frame_right.grid(row=0,column=1)
frame_right.grid_columnconfigure(0,weight=1)
frame_right.grid_columnconfigure(1,weight=2)
frame_right.grid_columnconfigure(2,weight=1)

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas, bg="yellow")
canvas.grid(row=0, column=0, sticky="news")

column_name1_label = tk.Label(frame_canvas, text="0 Added Songs")
column_name1_label.grid()
column_name1_label.grid(row=0, column=0)
column_name1_label.config(bg="green")
# Link a scrollbar to the canvas
vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)
frame_buttons = tk.Frame(canvas, bg="blue")
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

class New_Song:
    def __init__(self, song_name):
        print("added new song " + song_name)        
        new_song_label = tk.Label(frame_buttons, text=song_name)
        new_song_label.grid()
        delete_btn = tk.Button(frame_buttons, text="Remove", command= lambda: remove_song(song_name, new_song_label))
        delete_btn.grid()
        song_dict[song_name] = delete_btn
        print("add new song")
        new_song_label_dict[song_name] = new_song_label
        new_song_label.grid(row=row_count,column=0,sticky="ew",padx=5,pady=5)
        delete_btn.grid(row=row_count,column=1,sticky="ew",padx=5,pady=5)

def update_song_count(song_count):
    print(column_name1_label["text"])
    column_name1_label["text"] = str(song_count) + " Added Songs"
#    column_name1_label.pack()
    
def add_song():
    global row_count
    global download
    if download:
        return
    song_name = song_name_entry.get()
    singer_name = singer_name_entry.get()
    print("song name is " + song_name + " singer name is " + singer_name + " row is " + str(row_count))
    if len(singer_name)>0:
        song_id = song_name + " by " + singer_name
    else:
        song_id = song_name
    song_name_entry.delete(0,'end')
    singer_name_entry.delete(0,'end')
    if song_id in song_dict:
        print("song is already in dictionary")
        return
    if len(song_name)>0 and not (song_name in song_dict):  # new song
        New_Song(song_id)
        row_count += 1
    update_song_count(len(song_dict))
    canvas.config(scrollregion=canvas.bbox("all"))

def restart():
    global error_song
    global total_finished_song
    global finished_song
    global row_count
    global song_count
    global song_dict
    global download
    for keys,value in song_dict.items():
        value.destroy()
        del value
    for keys,value in new_song_label_dict.items():
        value.destroy()
        del value
    download = False
    total_finished_song += finished_song
    header_label["text"] = "Hi Jose, you downloaded " + str(total_finished_song) + " songs. Download some more!"
    song_count=0
    row_count=2
    finished_song=0
    error_song=0
    song_dict.clear()
    print("clear song dict")
    new_song_label_dict.clear()
    songify_btn["text"] = "Download Songs"
    column_name1_label["text"] = "0 Added Songs"
    
    
def remove_song(song_name, new_song_label):
    global row_count
    global song_dict
    global download
    if download:
        return
    print("remove a song " + song_name)
    remove_btn = song_dict[song_name]
    remove_btn.destroy()
    new_song_label.destroy()
    del song_dict[song_name]
    print("delete song")
    update_song_count(len(song_dict))

def update_ui():
    global download
    global song_dict
    global finished_song
    global error_song
    songify_btn["text"] = "Downloading ... Don\'t Close!"
    column_name1_label["text"] = "Downloading " + str(len(song_dict)) + " Songs"
    remain_song = len(song_dict) - error_song - finished_song
    while remain_song > 0:
        sleep(1)
        print("updatign ui")
        remain_song = len(song_dict) - error_song - finished_song
        if remain_song == 0:
            column_name1_label["text"] = "Download Finished!"
            songify_btn["text"] = "Finished. You may Remove the USB"   
        else: 
            column_name1_label["text"] = "Downloaded " + str(finished_song) + " Song. " + str(remain_song) + " left." 
    download = False
    restart()
    
def scrape_songs():
    global song_dict
    global finished_song
    global error_song
    ss = song_robot.SongScraper()
    for song in song_dict:
        try:
            url = ss.search_song(song)
            ss.download_song(url)
            finished_song += 1
            print("finished song")
        except:
            error_song += 1
            print("An error occurred, skipping song " + song)

def start_download():
    global download
    if download:
        return
    download = True
    robot_thread = Thread(target = scrape_songs)
    ui_thread = Thread(target = update_ui)
    ui_thread.start()
    robot_thread.start()

# v.pack(side="left", fill="y")

header_label = tk.Label(frame_right, text="Hi Jose. Download Songs!")
header_label.config(bg="orange")
header_label.grid(row=0, column=0, columnspan=2, sticky="news")
column_name2_label = tk.Label(frame_right, text="Add a Song")
column_name2_label.config(bg="green")
songify_btn = tk.Button(frame_right, text="Download Songs", command=start_download)

btn_add = tk.Button(frame_right, text="Add", command= add_song)

# song name entry
song_entry_label = tk.Label(frame_right,text="Song Name")
song_entry_label.config(bg="green")
song_name_entry = tk.Entry(frame_right)

# artist entry
singer_entry_label = tk.Label(frame_right,text="Singer Name")
singer_entry_label.config(bg="green")
singer_name_entry = tk.Entry(frame_right)

#test()

header_label.grid(row=0, sticky="ew",padx=5,pady=5, columnspan=3)
column_name1_label.grid(row=1,column=0,sticky="ew",padx=5,pady=5,columnspan=2)
column_name2_label.grid(row=1,column=3, sticky="ew",padx=5,pady=5, columnspan=2)

song_name_entry.grid(row=2,column=3,sticky="ew",padx=5,pady=5)
singer_name_entry.grid(row=3,column=3,sticky="ew",padx=5,pady=5)
song_entry_label.grid(row=2,column=2, sticky="ew",padx=5,pady=5)
singer_entry_label.grid(row=3,column=2, sticky="ew",padx=5,pady=5)

songify_btn.grid(row=4, column=3, sticky="ew", padx=5, pady=5, columnspan=2)
btn_add.grid(row=2,column=4,sticky="ew",padx=5,pady=5)
frame_canvas.config(width=650,
                    height=200)
# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))
window.mainloop()
