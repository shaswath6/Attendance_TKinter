import os
import os.path
import datetime
import pickle
import csv

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition

import util

from test import test

currentdate = datetime.datetime.now().strftime('%Y-%m-%d')

fp = open(currentdate+'.csv','w+',newline='')
lnwriter = csv.writer(fp)
lnwriter.writerow(['NAME','Time','Status','Class','Reg.NO'])

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title('attendance')
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)


        self.logout_button_main_window = util.get_button(self.main_window, 'logout', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)


        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def login(self):

        label = test(
            image=self.most_recent_capture_arr,
            model_dir='K:/tst/face attendance/spoof/resources/anti_spoof_models',
            device_id=0
        )

        if label == 1:

            name = util.recognize(self.most_recent_capture_arr, self.db_dir)

            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
            else:
                util.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
                b =str(format(name))
                print(b)
                fp = open('K:/tst/face attendance/'+b+'.pickle', 'rb')
                try:
                    while True:
                        a = pickle.load(fp)
                        c = a[1]

                except:
                    fp.close()
                util.msg_box('Admission id ! ','your id is'+c)

                with open(self.log_path, 'a') as f:
                    f.write('{} , {} , in , '.format(name, datetime.datetime.now())+c+'\n')
                    f.close()
                    lnwriter.writerow([name,datetime.datetime.now(),'in',c])

        else:
            util.msg_box('Hey, you are a spoofer!', 'You are fake !')
    def start(self):
        self.main_window.mainloop()
    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green',
                                                                      self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again',
                                                                         'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,
                                                                'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750, y=0)
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=80)

        self.text_label_register_new_no = util.get_text_label(self.register_new_user_window,
                                                                'Please, \ninput register number:')
        self.text_label_register_new_no.place(x=750, y=130)
        self.entry_text_register_new_no = util.get_entry_no(self.register_new_user_window)
        self.entry_text_register_new_no.place(x=750, y=210)

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

        util.msg_box('Success!', 'User was registered successfully !')

        self.register_new_user_window.destroy()
    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()


    def logout(self):

        label = test(
            image=self.most_recent_capture_arr,
            model_dir='K:/tst/face attendance/spoof/resources/anti_spoof_models',
            device_id=0
        )

        if label == 1:

            name = util.recognize(self.most_recent_capture_arr, self.db_dir)

            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
            else:
                util.msg_box('Hasta la vista !', 'Goodbye, {}.'.format(name))
                p = str(format(name))
                gp = open('K:/tst/face attendance/' + p + '.pickle', 'rb')
                try:
                    while True:
                        r = pickle.load(gp)
                        q = r[1]

                except:
                    gp.close()
                util.msg_box('Admission id ! ', 'your id is' + q)
                with open(self.log_path, 'a') as f:
                    f.write('{} , {} , out , '.format(name, datetime.datetime.now())+q+'\n')
                    f.close()
                    lnwriter.writerow([name, datetime.datetime.now(), 'out',q])

        else:
            util.msg_box('Hey, you are a spoofer!', 'You are fake !')

#
app = App()
app.start()
# fp = open('K:/tst/face attendance/db/shaswath.pickle','rb')
# try:
#     while True:
#         a= pickle.load(fp)
#         print(a)
# except:
#     fp.close()