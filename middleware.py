
import pymongo
from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk
from larger_port_user import large_port
from smaller_port_user import small_port

def middleware(currentuser):
    userdata = MongoClient()
    mydb = userdata["Userdata"]
    savedata = mydb["users"]
    currentuser['state'] = 1
    savedata.save(currentuser)
    userlist = []
    states = []
    for x in savedata.find():
        if(x['name'] == currentuser['name']):
            continue
        else:
            if(x['state'] == 0):
                userlist.append(x['name']+", Offline") 
            elif(x['state'] == 1):
                userlist.append(x['name']+", Online") 

    

    def go(*args): 
        l = comboExample.get()
        usr = l.split(', ')[0]
        usr_state = l.split(', ')[1]
        for x in savedata.find():
            if(x['name'] == usr):
                the_choosen = x
        if(int(the_choosen['port']) > int(currentuser['port'])):
            app.destroy()
            small_port(the_choosen, currentuser)
        
        elif(int(the_choosen['port']) < int(currentuser['port'])):
            app.destroy()
            large_port(currentuser, the_choosen)
        else:
            print("dump")

    app = tk.Tk() 
    app.geometry('400x300')
    labelTop = tk.Label(app, text = "Who do you want to chat with?")
    labelTop.pack(anchor=tk.NE)
    comboExample = ttk.Combobox(app, values = userlist,state="readonly")
    comboExample.pack(anchor=tk.NE)
    comboExample.current(0)
    comboExample.bind("<<ComboboxSelected>>",go)   

    def on_closing():
        currentuser['state'] = 0
        savedata.save(currentuser)
        app.destroy()
    
    while(True):
        app.protocol("WM_DELETE_WINDOW", on_closing)
        app.mainloop()

    
