import os
import pickle
from customtkinter import *
import tkinter as tk
from tkinter import messagebox
import face_recognition
from PIL import Image

def get_button(window, text, color, command, ):
    button = CTkButton(window,
                       text=text,
                       corner_radius=90,
                       border_color='white',
                       border_width=2,
                       height=50,



                       command=command,

                       fg_color='transparent',
                       hover_color=color,
                       font=('Helvetica bold', 25))


    return button
def get_button2(window, text, color, command, ):
    button = CTkButton(window,
                       text=text,
                       corner_radius=90,
                       border_color='black',
                       border_width=2,
                       height=50,
                       text_color='black',



                       command=command,

                       fg_color='transparent',
                       hover_color=color,
                       font=('Helvetica bold', 25))


    return button
def frame_(window,text):
    frame = CTkScrollableFrame(window,fg_color='white',border_color='black',border_width=2,orientation='vertical',scrollbar_button_color='grey',height=800,width=1200)
    frame.pack(expand=True)
    label = CTkLabel(frame, text=text, font=("Times", 32), text_color='black', justify="left")
    a = label.pack(anchor='s',expand = True,pady=1,padx=1)
    return a





def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_button_gaisss(window  ):
    # img = Image.open('K:/tst/gaisss.png')
    # Gbutton = CTkButton(window,
    #
    #                    corner_radius=32,
    #                    border_color='white',
    #                    border_width=2,
    #                     width=300,
    #
    #
    #
    #                    fg_color='transparent',
    #                    hover_color=color,
    #                     image=CTkImage(light_image=img)
    #                    )
    img = CTkImage(dark_image=Image.open("K:/tst/Attendance_TKinter/gaisss.png"),size=(500,90))
    Gbutton = CTkButton(window,image= img,text = " ",fg_color='transparent',hover_color='black')
    return Gbutton



def get_text_label(window, text):
    label = CTkLabel(window, text=text,font=("Times", 32), justify="left")

    return label
def get_text_label2(window, text):
    label = CTkLabel(window, text=text,font=("Times", 32), text_color='black', justify="left")

    return label


def get_entry_text(window):
    inputtxt = CTkTextbox(window,
                         corner_radius=16,
                         border_width=2,
                         height=10,
                          width= 300,
                         font=('Times',28),
                         border_color='white')
    return inputtxt

def get_entry_no(window):
    inputno = CTkTextbox(window,
                         corner_radius=16,
                         border_width=2,
                         height=10,
                         width= 300,
                         font=('Times',28),
                         border_color='white')
    return inputno

def msg_box(title, description):
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'