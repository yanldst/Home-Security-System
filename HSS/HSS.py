import RPi.GPIO as GPIO
import time
import os
import socket
import fcntl
import struct
import smtplib
import picamera
import datetime
import sqlite3
import spidev
import dropbox
client = dropbox.client.DropboxClient('Dropbox_token_key')

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

door_pin = 23
motion_pin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(motion_pin, GPIO.IN)
GPIO.setup(door_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)


def door_state():
    if GPIO.input(door_pin):
        return 1
    else:
        return 0

def motion_state():
    if GPIO.input(motion_pin):
        return 1
    else:
        return 0

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def send_email(subject, body):
    smtpUser = 'email_address'
    smtpPass = 'email_password'

    toAdd = 'email_to_receive_message'
    fromAdd = smtpUser
    header = 'To: ' + toAdd + "\n" + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject

    s = smtplib.SMTP('smtp.gmail.com',587)

    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(smtpUser, smtpPass)
    s.sendmail(fromAdd, toAdd, header + '\n\n' + body)

    s.quit()
    
def getCurrentMode():
    cur.execute('SELECT * FROM myapp_mode')
    data = cur.fetchone()  # (1, u'auto')
    return data[1]

while True:
    subject = 'Alert: your apartment is in danger'
    body = ''
    option = getCurrentMode()
    
    if motion_state() and door_state():

        body += 'You door is opened and motion detected!\n'
        if option == 'stream':
            body += 'Please watch video stream at http://' + get_ip_address('wlan0') + ':8080/html/\n'
        elif option == 'photos':
            body += 'Please check photos in your Dropbox!\n'

        while motion_state() and door_state():

            if option == 'stream':
                send_email(subject, body)
                while True:
                    if not (motion_state() and door_state()):
                        os.system('/home/pi/RPi_Cam_Web_Interface/RPi_Cam_Web_Interface_Installer.sh stop')
                        break
                    os.system('/home/pi/RPi_Cam_Web_Interface/RPi_Cam_Web_Interface_Installer.sh start')
                    time.sleep(15)
                    os.system('clear')
            elif option == 'photos':
                os.system('/home/pi/RPi_Cam_Web_Interface/RPi_Cam_Web_Interface_Installer.sh stop')
                os.system('clear')
                send_email(subject, body)
                count = 1
                photos_path = '/home/pi/Home Security/photo/img' + str(count) + '.jpg'
                Folder = time.strftime("%H-%M-%S_%d-%m-%Y")
                response = client.file_create_folder(Folder)
                camera = picamera.PiCamera()
                while True:
                    if not (motion_state() and door_state()):
                        camera.close()
                        break
                    camera.capture(photos_path)
                    f = open(photos_path, 'rb')
                    response = client.put_file('/' + Folder + '/img' + str(count) + '.jpg', f)
                    os.remove(photos_path)
                    count += 1
                    time.sleep(5)








        
        
