import os
import os.path
import datetime
import pickle
import csv
from customtkinter import *
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition

import pqr

from test import test

currentdate = datetime.datetime.now().strftime('%Y-%m-%d')

ap = open(currentdate+'.csv','w+')
obj = csv.writer(ap)
obj.writerow(['NAME','Date-Time','Status','Reg.NO'])
ap.close()

class App:
    def __init__(self):
        self.main_window = CTk()
        self.main_window.title('ATTENDANCE')
        self.main_window.geometry("1200x520+350+100")
        set_appearance_mode('dark')

        self.button_main_window_gaisss = pqr.get_button_gaisss(self.main_window)
        self.button_main_window_gaisss.place(relx=0.78, rely=0.15, anchor='center')

        self.login_button_main_window = pqr.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(relx=0.8, rely=0.45,anchor='center')


        self.logout_button_main_window = pqr.get_button(self.main_window, 'logout', 'red', self.logout)
        self.logout_button_main_window.place(relx=0.8, rely=0.6,anchor='center')

        self.register_new_user_button_main_window = pqr.get_button(self.main_window, 'register new user', 'blue',
                                                                    self.register_new_user)
        self.register_new_user_button_main_window.place(relx=0.8, rely=0.75,anchor='center')

        self.log_button_main_window = pqr.get_button(self.main_window, 'Show log', 'yellow', self.log)
        self.log_button_main_window.place(relx=0.8, rely=0.9, anchor='center')

        self.webcam_label = pqr.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=640, height=480)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def login(self):

        label = test(
            image=self.most_recent_capture_arr,
            model_dir='K:/tst/Attendance_TKinter/face attendance/spoof/resources/anti_spoof_models',
            device_id=0
        )

        if label == 1:

            name = pqr.recognize(self.most_recent_capture_arr, self.db_dir)

            if name in ['unknown_person', 'no_persons_found']:
                pqr.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
            else:
                self.login_window = CTkToplevel(self.main_window)
                self.login_window.geometry('1200x530+350+100')
                set_appearance_mode('dark')
                self.login_window.wm_attributes('-topmost', True)
                self.img_ = pqr.get_img_label(self.login_window)
                self.img_.place(x=10,y=0,width=700,height=500)
                self.add_img_to_label(self.img_)

                # pqr.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
                b =str(format(name))
                print(b)
                fp = open('K:/tst/Attendance_TKinter/face attendance/'+b+'.pickle', 'rb')
                try:
                    while True:
                        a = pickle.load(fp)
                        c = a[1]

                except:
                    fp.close()
                # pqr.msg_box('Admission id ! ','your id is'+c)
                self.text_login = pqr.get_text_label2(self.login_window,
                                                     'Welcome Back ! \n' + b)
                self.text_login.place(x=750,y = 100)
                self.text_login = pqr.get_text_label2(self.login_window,
                                                      'Your id is, \n' + c)
                self.text_login.place(x=750, y=200)

                self.close_button =pqr.get_button2(self.login_window, 'CLOSE',
                                                                         'red', self.close_user_login)
                self.close_button.place(x=850,y=400)

                with open(self.log_path, 'a') as f:
                    z = ''
                    for i in range(15-len(name)):
                        z+=' '




                    f.write('{}'.format(name)+z+'***   {}   ***        in         ***        '.format( datetime.datetime.now())+c+'\n')

                    f.close()
                    up = open(currentdate+ '.csv', 'a', newline='')
                    obj = csv.writer(up)
                    obj.writerow([name,datetime.datetime.now(),'in',c])
                    up.close()

        else:
            # pqr.msg_box('Hey, you are a spoofer!', 'You are fake !')
            self.msg_window = CTkToplevel(self.main_window)
            self.msg_window.geometry('400x250+600+300')
            set_appearance_mode('dark')
            self.msg_window.wm_attributes('-topmost', True)
            self.text_msg = pqr.get_text_label2(self.msg_window, '      No user Found\n               or\n   You are spoofing !'
                                                )
            self.text_msg.place(x=50, y=50)
            self.close_button = pqr.get_button2(self.msg_window, 'CLOSE',
                                                'red', self.close_user_msg)
            self.close_button.place(relx=0.5, rely=0.80, anchor='center')
    def logout(self):

        label = test(
            image=self.most_recent_capture_arr,
            model_dir='K:/tst/Attendance_TKinter/face attendance/spoof/resources/anti_spoof_models',
            device_id=0
        )

        if label == 1:

            name = pqr.recognize(self.most_recent_capture_arr, self.db_dir)

            if name in ['unknown_person', 'no_persons_found']:
                pqr.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
            else:
                self.logout_window = CTkToplevel(self.main_window)
                self.logout_window.geometry('1200x530+350+100')
                set_appearance_mode('dark')
                self.logout_window.wm_attributes('-topmost', True)
                self.img_ = pqr.get_img_label(self.logout_window)
                self.img_.place(x=10, y=0, width=700, height=500)
                self.add_img_to_label(self.img_)
                # pqr.msg_box('Hasta la vista !', 'Goodbye, {}.'.format(name))
                p = str(format(name))
                gp = open('K:/tst/Attendance_TKinter/face attendance/' + p + '.pickle', 'rb')
                try:
                    while True:
                        r = pickle.load(gp)
                        q = r[1]

                except:
                    gp.close()
                # pqr.msg_box('Admission id ! ', 'your id is' + q)
                self.text_logout = pqr.get_text_label2(self.logout_window,
                                                      'Thank you!!! \n' + p)
                self.text_logout.place(x=750, y=100)
                self.text_logout = pqr.get_text_label2(self.logout_window,
                                                      'Your id is, \n' + q)
                self.text_logout.place(x=750, y=200)
                self.close_button = pqr.get_button2(self.logout_window, 'CLOSE',
                                                    'red', self.close_user_logout)
                self.close_button.place(x=850, y=400)
                with open(self.log_path, 'a') as f:
                    z = ''
                    for i in range(15 - len(name)):
                        z += ' '
                    f.write('{}'.format(name)+z+'***   {}   ***        out        ***        '.format( datetime.datetime.now())+q+'\n')
                    f.close()
                    jp = open(currentdate + '.csv', 'a', newline='')
                    obj = csv.writer(jp)
                    obj.writerow([name, datetime.datetime.now(), 'out',q])
                    jp.close()

        else:
            # pqr.msg_box('Hey, you are a spoofer!', 'You are fake !')
            self.msg_window = CTkToplevel(self.main_window)
            self.msg_window.geometry('400x250+600+300')
            set_appearance_mode('dark')
            self.msg_window.wm_attributes('-topmost', True)
            self.text_msg = pqr.get_text_label2(self.msg_window, '      No user Found\n               or\n   You are spoofing !'
                                                )
            self.text_msg.place(x=50, y=50)
            self.close_button = pqr.get_button2(self.msg_window, 'CLOSE',
                                                'red', self.close_user_msg)
            self.close_button.place(relx=0.5, rely=0.80, anchor='center')


    def log(self):
        self.log_window = CTkToplevel(self.main_window)
        self.log_window.geometry('1920x1080+0+0')
        set_appearance_mode('dark')
        self.log_window.wm_attributes('-topmost', True)
        mp = open('K:/tst/Attendance_TKinter/face attendance/log.txt', 'r')
        data = mp.read()
        self.text_log = pqr.frame_(self.log_window,
                                              data)
        self.text_log = pqr.get_text_label2(self.log_window,
                                              'NAME                                  Date-Time                           Status                    Reg.No')
        self.text_log.place(x=420, y=50)

        self.close_button = pqr.get_button2(self.log_window, 'CLOSE',
                                            'red', self.close_user_log)
        self.close_button.place(relx=0.5, rely=0.94, anchor='center')

    def start(self):
        self.main_window.mainloop()

    def close_user_login(self):
        self.login_window.destroy()

    def close_user_logout(self):
        self.logout_window.destroy()
    def close_user_log(self):
        self.log_window.destroy()
    def close_user_msg(self):
        self.msg_window.destroy()
    def register_new_user(self):
        self.register_new_user_window = CTkToplevel(self.main_window)
        self.register_new_user_window.geometry("1200x720+370+120")
        self.main_window.title('ATTENDANCE')
        set_appearance_mode('dark')
        self.register_new_user_window.wm_attributes('-topmost',True)

        self.accept_button_register_new_user_window = pqr.get_button(self.register_new_user_window, 'Accept', 'green',
                                                                      self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(relx=0.25, rely=0.82,anchor = 'center')

        self.try_again_button_register_new_user_window = pqr.get_button(self.register_new_user_window, 'Try again',
                                                                         'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(relx=0.750, rely=0.82,anchor = 'center')

        self.capture_label = pqr.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=640, height=480)
        self.text_label_register_new_user = pqr.get_text_label(self.register_new_user_window,
                                                                'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750, y=20)
        self.entry_text_register_new_user = pqr.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=110)

        self.text_label_register_new_no = pqr.get_text_label(self.register_new_user_window,
                                                                'Please, \ninput register number:')
        self.text_label_register_new_no.place(x=750, y=200)
        self.entry_text_register_new_no = pqr.get_entry_no(self.register_new_user_window)
        self.entry_text_register_new_no.place(x=750, y=290)

        self.add_img_to_label(self.capture_label)





    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()
    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)
    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        no = self.entry_text_register_new_no.get(1.0,"end-1c")

        embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

        file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')
        pickle.dump(embeddings, file)
        cp = open(str(name)+'.pickle','wb')
        pickle.dump([name,no],cp)

        pqr.msg_box('Success!', 'User was registered successfully !')

        self.register_new_user_window.destroy()
    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()




    # def msg_box(self):
    #     self.msg_window = tk.Toplevel(self.main_window)
    #     self.msg_window.geometry('200x100')
    #     self.text_msg = pqr.get_text_label2(self.msg_window,'Hey, you are a spoofer!\n You are fake !'
    #                                            )
    #     self.text_msg.place(x=50,y=50)


#
app = App()
app.start()