# coding: utf-8
import tkinter as tk 
from tkinter import messagebox
from pymongo import MongoClient
from middleware import middleware

userdata = MongoClient()

def encrypt(key, s): 
    b = bytearray(str(s).encode("gbk")) 
    n = len(b)
    c = bytearray(n*2) 
    j = 0 
    for i in range(0, n): 
        b1 = b[i] 
        b2 = b1 ^ key
        c1 = b2 % 16 
        c2 = b2 // 16
        c1 = c1 + 65 
        c2 = c2 + 65
        c[j] = c1 
        c[j+1] = c2 
        j = j+2 
    return c.decode("gbk") 
 
def decrypt(key, s): 
    c = bytearray(str(s).encode("gbk")) 
    n = len(c)
    if n % 2 != 0 : 
        return "" 
    n = n // 2 
    b = bytearray(n) 
    j = 0 
    for i in range(0, n): 
        c1 = c[j] 
        c2 = c[j+1] 
        j = j+2 
        c1 = c1 - 65 
        c2 = c2 - 65 
        b2 = c2*16 + c1 
        b1 = b2^ key 
        b[i]= b1 
    try: 
        return b.decode("gbk") 
    except: 
        return ("failed")

mydb = userdata["Userdata"]
savedata = mydb["users"]
currentportvalue = 10000
fileportnumber = 40000
for x in savedata.find():
    if(x['port'] == currentportvalue):
        currentportvalue = currentportvalue + 1
        fileportnumber = fileportnumber + 1

window = tk.Tk()
window.title('Registration')
window.geometry('500x300')
tk.Label(window,text='User name: ').place(x=50,y=50)
tk.Label(window,text='Password: ').place(x=50,y=80)
var_usr_name = tk.StringVar()
entry_usr_name = tk.Entry(window,textvariable=var_usr_name)
entry_usr_name.place(x=150,y=50)
var_usr_passwd = tk.StringVar()
entry_usr_passwd = tk.Entry(window,textvariable=var_usr_passwd,show='*')
entry_usr_passwd.place(x=150,y=80)

def usr_login():
    usrs_name = var_usr_name.get()
    password_check = var_usr_passwd.get()
    currentuser = None
    for x in savedata.find():
        if(x['name'] == usrs_name):
            currentuser = x
    print(currentuser)
    if (currentuser == None):
        is_signed_up = tk.messagebox.askyesno('Welcome', 'You may not sign up, please sign up at first')
        if(is_signed_up):
            usr_signup()
    elif(encrypt(12, password_check) != currentuser['password']):
            tk.messagebox.showerror(title='Sign in', message='Error! Your password and confirm password is not the same')
    else:
        tk.messagebox.showinfo(title="Login",message="Successfully login")
        window.destroy()
        middleware(currentuser)

def usr_signup():
    def Registration_signup():
        global currentportvalue
        global fileportnumber
        np = new_passwd.get()
        npf = new_passwd_confirm.get()
        nn = new_name.get()
        ifuserexit = 0        
        for x in savedata.find():
            if(x['name'] == nn):
                ifuserexit = 1
        if((np=='') or (npf =='') or (nn =='')):
            tk.messagebox.showerror(
                title='Sign up', message='Error! Please fill in all the blanks')
        else:
            if(np != npf):
                tk.messagebox.showerror(
                    title='Sign up', message='Error! Your password and confirm password is not the same')
            elif(ifuserexit == 1):
                tk.messagebox.showerror(
                    title='Sign up', message='Error! The sign up information has already existed')          
            else:
                newuser = {"name": nn, "port": currentportvalue, "fileport": fileportnumber, "password": encrypt(12, npf), "state": 0}
                
                x = savedata.insert_one(newuser)
                currentportvalue = currentportvalue + 1
                fileportnumber = fileportnumber + 1
                tk.messagebox.showinfo(
                    'Welcome', 'You have successfully signed up!')
                window_signup.destroy()       
    window_signup = tk.Toplevel(window)
    window_signup.geometry("350x200")
    window_signup.title('Sign up window')
    new_name = tk.StringVar()
    tk.Label(window_signup,text='User name: ').place(x=10,y=10)
    entry_new_name = tk.Entry(window_signup,textvariable=new_name)
    entry_new_name.place(x=150,y=10)
    new_passwd = tk.StringVar()
    tk.Label(window_signup,text='Password: ').place(x=10,y=50)
    enetry_new_passwd = tk.Entry(window_signup,textvariable=new_passwd,show="*")
    enetry_new_passwd.place(x=150,y=50)
    new_passwd_confirm = tk.StringVar()
    tk.Label(window_signup,text='Confirm Password: ').place(x=10,y=90)
    entry_new_conf_passwd = tk.Entry(window_signup,textvariable=new_passwd_confirm,show="*")
    entry_new_conf_passwd.place(x=150,y=90)
    btn_commfirm_sign_up = tk.Button(window_signup,text="Submit",command=Registration_signup)
    btn_commfirm_sign_up.place(x=150,y=130)
    
    def signup_exitquit():
        window_signup.destroy()

    btn_exit = tk.Button(window_signup,text="Exit",command=signup_exitquit)
    btn_exit.place(x=250,y=130)

def exitquit():
    if (var_usr_name.get() == "" or var_usr_passwd.get() == ""):
        pass
    window.destroy()

btn_login = tk.Button(window,text="Login",command=usr_login)
btn_login.place(x=100,y=200)
btn_signup =  tk.Button(window,text="Sign up",command=usr_signup)
btn_signup.place(x=200,y=200)
btn_exit = tk.Button(window,text="Exit",command=exitquit)
btn_exit.place(x=300,y=200)
window.mainloop()



