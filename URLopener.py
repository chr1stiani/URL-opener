from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tkinter import *
import threading

# Function to open and close the URL
def browse(url, num_visits, stop_event):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Enable incognito mode
    chrome_options.add_argument("--headless")  # Enable headless mode
    prefs = {"profile.managed_default_content_settings.images": 2,  # Disable images
             "profile.managed_default_content_settings.javascript": 2}  # Disable JavaScript
    chrome_options.add_experimental_option("prefs", prefs)

    for _ in range(num_visits):
        # Check if stop event is set
        if stop_event.is_set():
            break

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        driver.quit()

# Function to get input from the UI and call the browse function
def start_browsing():
    url = url_entry.get()
    num_visits = int(visits_entry.get())
    # Create a stop event
    stop_event = threading.Event()
    # Run the browse function in a separate thread
    thread = threading.Thread(target=browse, args=(url, num_visits, stop_event))
    thread.start()
    # Store the stop event and thread in the root object for later access
    root.stop_event = stop_event
    root.thread = thread

# Function to stop the browsing process
def stop_browsing():
    # Set the stop event to stop the browsing thread
    root.stop_event.set()
    # Wait for the thread to finish
    root.thread.join()

# Create the UI
root = Tk()

Label(root, text="URL:").grid(row=0)
Label(root, text="Number of visits:").grid(row=1)

url_entry = Entry(root)
visits_entry = Entry(root)

url_entry.grid(row=0, column=1)
visits_entry.grid(row=1, column=1)

Button(root, text="Start", command=start_browsing).grid(row=2, column=1, sticky=W, pady=4)
Button(root, text="Stop", command=stop_browsing).grid(row=2, column=2, sticky=W, pady=4)

mainloop()
