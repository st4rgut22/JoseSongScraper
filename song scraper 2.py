import tkinter as tk
window = tk.Tk()
greeting = tk.Label(text="Hi Jose. Enter Song Names Below")
greeting.pack()
song_title_list = []

added_song_frame = tk.Frame()
to_add_song_frame = tk.Frame()
song_library = tk.Label(text="Song Library: " + str(len(song_title_list)) + " songs", master=added_song_frame)

song_library_text = ""


def removeSong():
    # TODO
    print("remove song")

def addSong(): 
    song_title = new_song_entry.get()
    song_title_list.append(song_title)
    # clear entry
    New_Song(song_title)
    
class New_Song:
    def __init__(self, song_name):
        print("added new song " + song_name)
        new_song_label = tk.Label(master=added_song_frame)
        delete_btn = tk.Button(text="Remove Song", width=25, height=5, bg="red",
                               command=removeSong, master=added_song_frame)
        new_song_label.pack()
        delete_btn.pack()

new_song_entry = tk.Entry(master=to_add_song_frame)
new_song_entry.pack()
add_song_btn = tk.Button(text="add Song", width=25, height=5, bg="blue",
                         command=addSong, master=to_add_song_frame)

song_library.pack()
add_song_btn.pack()

added_song_frame.pack()
to_add_song_frame.pack()
window.mainloop()

