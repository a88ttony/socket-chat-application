# socket chat application
This is the repository of Computer Networks final project. We develop a UDP chatting and FTP file transfer application with sockets in Python, which supports following functionalities

* Registration with encrypted password
* Online and offline messaging
* File transfer
* Historical messages
* User interface

## How to Run
1. Install and run mongodb
2. Run the chat application with `$ python3 registration.py`

## Demo
* **Sign up** - create account with unique username      
<div align=center><img width="400" src="https://github.com/a88ttony/socket-chat-application/blob/master/demo_image/signup_error.png"/></div>  
<br/> 

* **Online status** - the application shows friends' online status, and you can choose the user that you want to chat with from the friends lists no matter they are online or offline  
 
<div align=center><img width="400" src="https://github.com/a88ttony/socket-chat-application/blob/master/demo_image/choose_friend.png"/></div>
<br/>     
 
* **Online/Offline messaging and historical messages** - the application supports online and offline messaging, and it stores all your chatting history with other users  
  
<div align=center><img width="800" src="https://github.com/a88ttony/socket-chat-application/blob/master/demo_image/chatting_history.png"/></div>
<br/>   
    
* **File transfer** - the application also supports file transfer, and you can send multiple files to other user at a time if they are online
  
<div align=center><img width="400" src="https://github.com/a88ttony/socket-chat-application/blob/master/demo_image/file_transfer.png"/></div>
<br/>  
    
* **Default file receiver** - the application will createa default folder ```downloads``` for the receiver to store receiving files
  
<div align=center><img width="400" src="https://github.com/a88ttony/socket-chat-application/blob/master/demo_image/receive_file.png"/></div>
