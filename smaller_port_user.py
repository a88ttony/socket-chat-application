import pymongo
from pymongo import MongoClient
import socket
import sys
import select
import threading
import time
import json
import tkinter
import signal
import atexit
import os,struct
from tkinter import filedialog
import socketserver, _thread

userdata = MongoClient()
mydb = userdata["Userdata"]
savedata = mydb["users"]
messageslist = []
i = 0
message = {}

def small_port(large_item, small_item):
    large_user = large_item['name']
    small_user = small_item['name']
    large_port = large_item['port']
    small_port = small_item['port']
    largefile_port = large_item['fileport']
    smallfile_port = small_item['fileport']

    print("large: %d" % large_port)
    print("small: %d" % small_port)

    top = tkinter.Tk()
    top.title("Chatting with - "+large_user)
    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  
    scrollbar = tkinter.Scrollbar(messages_frame)  
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()
    userdata = MongoClient()
    mydb = userdata["chatHistory"]
    dbname = large_user + small_user
    history = mydb[dbname]
    for x in history.find():
        if(x['name'] == large_user):
            msg = x['name'] + ":  " + x['chat']
            msg_list.insert(tkinter.END, msg)
            msg_list.see(tkinter.END) 
        else:
            msg = " I:  " + x['chat']
            msg_list.insert(tkinter.END,msg)
            msg_list.see(tkinter.END)

    def client():
        global i
        global message
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(False) 
        inputs = [s]
 
        def send(event=None):  
            global i, message
            sendmessa = " I: "+my_msg.get()
            msg_list.insert(tkinter.END, sendmessa)
            msg_list.see(tkinter.END)
            message = {"number": i, "name": small_user, "chat": my_msg.get()}
            s.sendto(my_msg.get().encode('utf-8'), ('127.0.0.1', large_port))
            i = i+1
            my_msg.set("")  
        
        entry_field = tkinter.Entry(top, textvariable=my_msg)
        entry_field.bind("<Return>", send) 
        entry_field.pack()
        send_button = tkinter.Button(top, text="Send", command=send)
        send_button.pack()
        file_button = tkinter.Button(top, text="File", command=send_file)
        file_button.place(x=400,y=270,anchor='nw')

    def server():
        print("test")
        global i
        global message
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('127.0.0.1', small_port))
        s.setblocking(0)
        while True:
            try:
                data, addr = s.recvfrom(1024)
                msg = large_user+": "+data.decode('utf-8')
                msg_list.insert(tkinter.END, msg)
                msg_list.see(tkinter.END)
                time.sleep(1)

            except:
                continue  

    def upload():
        global i
        global message
        j=0
        userdata = MongoClient()
        mydb = userdata["chatHistory"]
        dbname = large_user + small_user
        history = mydb[dbname]
        while True:
            try:  
                if i > j:
                    x = history.insert_one(message)
                    j=j+1
            except:
                continue


    def send_file():
        if(small_item['state'] == 0):
            msg = large_user+" is not available now!"
            msg_list.insert(tkinter.END, msg)
        elif(small_item['state'] == 1):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(('127.0.0.1', largefile_port))
            
            while True:
                root = tkinter.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilenames()
                print(file_path)
                for filedir in file_path:
                    if os.path.isfile(filedir):
                        fileinfo_size=struct.calcsize('128sl') 
        
                        fhead = struct.pack('128sl', bytes(os.path.basename(filedir).encode('utf-8')),os.stat(filedir).st_size);

                        s.send(fhead) 
                        print ('Chosen File: ',filedir)
                        fo = open(filedir,'rb')
                        while True:
                            filedata = fo.read(1024)
                            if not filedata:
                                break
                            s.send(filedata)
                        fo.close()
                        print ('File Sending Done...')
                s.close()
                break

    #-*- coding: UTF-8 -*-
    def recv():
        host ='127.0.0.1'
        port = smallfile_port
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        s.bind((host,port)) 
        s.listen(5)

        download_dir = r'./downloads'
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)

        while True:
            print("Listening")
            connection,address=s.accept()
            print('Connected by ',address)
            def conn_thread(connection,address): 
                while True:
                    try:
                        fileinfo_size=struct.calcsize('128sl') 
                        buf = connection.recv(fileinfo_size)
                        if buf: #
                            filename,filesize = struct.unpack('128sl',buf) 
                            filename_f = filename.decode().strip('\00')
                            filenewname = os.path.join('./downloads/',('new_'+ filename_f))
                            msg = "received file: "+ filenewname+ ", and filesize is "+ str(filesize)
                            msg_list.insert(tkinter.END,msg)
                            msg_list.see(tkinter.END)
                            recvd_size = 0 
                            file = open(filenewname,'wb')
                            print ('stat receiving...')
                            while not recvd_size == filesize:
                                if filesize - recvd_size > 1024:
                                    rdata = connection.recv(1024)
                                    recvd_size += len(rdata)
                                else:
                                    rdata = connection.recv(filesize - recvd_size) 
                                    recvd_size = filesize
                                file.write(rdata)
                            file.close()
                            print ('receive done')
                    except socket.timeout:
                        connection.close()
            _thread.start_new_thread(conn_thread,(connection,address)) 
        s.close()

    def on_closing():
        small_item['state'] = 0
        savedata.save(small_item)
        top.destroy()

    def tk():
        x = threading.Thread(target=client)
        y = threading.Thread(target=server)
        z = threading.Thread(target=upload)
        v = threading.Thread(target=recv)
        x.start()
        y.start()
        z.start()
        v.start()
        while(True):
            top.protocol("WM_DELETE_WINDOW", on_closing)
            tkinter.mainloop() 

    tk()






