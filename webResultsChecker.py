import tkinter as tk
from tkinter import messagebox, scrolledtext
import webbrowser
from urllib.request import Request, urlopen
import hashlib
import time
from win11toast import toast
import threading

stop_flag = False  # Global flag to control the loop
current_url = ''

def checker(url_to_request, output_text):
    global stop_flag
    try:
        url = Request(url_to_request, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(url).read()
        current_hash = hashlib.sha224(response).hexdigest()
        output_text.insert(tk.END, "Constantly checking the website for updates...\n")
        toast('Constantly checking the website for updates...',
                           'Click to open URL on your own.'
                           , on_click=url_to_request)
        time.sleep(10)

        while not stop_flag:
            response = urlopen(url).read()
            new_hash = hashlib.sha224(response).hexdigest()

            if new_hash == current_hash:
                time.sleep(30)
                continue

            else:
                message = "Something changed on the website " + url_to_request + ". You can check."
                print(message)
                output_text.insert(tk.END, message + "\n")
                toast('Update! Something changed on the website.',
                                   'Click to open URL.',
                                   on_click=url_to_request)
                current_hash = new_hash
                time.sleep(30)

        output_text.insert(tk.END, "Checking stopped.\n")

    except Exception as e:
        error_message = "An error occurred. Read: " + str(e)
        print(error_message)
        output_text.insert(tk.END, error_message + "\n")

def open_website(output_text):
    global stop_flag
    stop_flag = False  # Reset the stop flag
    url = entry.get()
    global current_url
    current_url = url

    if url:
        # Start the checker function in a new thread
        threading.Thread(target=checker, args=(url, output_text), daemon=True).start()
    else:
        messagebox.showerror("Error", "Please enter a valid URL.")

def openInBrowser():
    global current_url
    webbrowser.open(current_url)

def stop_checking(output_text):
    global stop_flag
    stop_flag = True
    output_text.insert(tk.END, "Stopped checking for updates." + "\n")

# Create the main window
root = tk.Tk()
root.title("Website Checker")

# Create and place the entry widget
entry = tk.Entry(root, width=40)
entry.pack(pady=10)

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", command=lambda: open_website(text_area))
submit_button.pack()

# Create a button to stop checking
stop_button = tk.Button(root, text="Stop Checking", command=lambda: stop_checking(text_area))
stop_button.pack()

# Create a scrolled text area
text_area = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD)
text_area.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
