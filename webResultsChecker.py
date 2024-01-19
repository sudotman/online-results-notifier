import time
import hashlib
from urllib.request import urlopen, Request
from win11toast import toast
import webbrowser
import tkinter as tk
from tkinter import messagebox
 
urlToRequest = 'https://ugcnet.nta.nic.in/'
# setting the URL you want to monitor
url = Request(urlToRequest, headers={'User-Agent': 'Mozilla/5.0'})
 
# to perform a GET request and load the
# content of the website and store it in a var
response = urlopen(url).read()
 
def testFunc():
    webbrowser.open(urlToRequest)
 
# to create the initial hash
currentHash = hashlib.sha224(response).hexdigest()
print("Constantly checking the website for updates...")
toast('Constantly checking the website for updates...', 'Click to open url on your own.', on_click=testFunc())
time.sleep(10)
while True:
    try:
        # perform the get request and store it in a var
        response = urlopen(url).read()
 
        # create a hash
        currentHash = hashlib.sha224(response).hexdigest()
 
        # wait for 30 seconds
        time.sleep(30)
 
        # perform the get request
        response = urlopen(url).read()

        # create a new hash
        newHash = hashlib.sha224(response).hexdigest()
 
        # check if new hash is same as the previous hash
        if newHash == currentHash:
            continue
 
        # if something changed in the hashes
        else:
            # notify
            print("Something changed on the website " + urlToRequest + ". You can check.")

            toast('Update! Something changed on the website.', 'Click to open url.', on_click=testFunc())
 
            # again read the website
            response = urlopen(url).read()
 
            # create a hash
            currentHash = hashlib.sha224(response).hexdigest()
 
            # wait for 30 seconds
            time.sleep(30)
            continue
 
    # To handle exceptions
    except Exception as e:
        print("An error occured. Read: " + e)

