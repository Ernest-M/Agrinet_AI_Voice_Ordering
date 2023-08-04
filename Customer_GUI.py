from helperFunctions import *
import tkinter as tk
from tkinter import ttk
import pyaudio
import wave
import sounddevice as sd
import soundfile as sf

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
recording = False
frames_list = []

def start_recording():
    global recording, frames_list, audio_stream
    recording = True
    frames_list = []
    audio_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    stream_callback()

def stream_callback():
    global recording, frames_list, audio_stream
    if recording:
        data = audio_stream.read(CHUNK)
        frames_list.append(data)
        app.after(int(1000 / (RATE / CHUNK)), stream_callback)

def stop_recording():
    global recording, audio_stream
    recording = False
    audio_stream.stop_stream()
    audio_stream.close()
    save_recording()

def save_recording():
    global frames_list
    wf = wave.open("output.wav", "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames_list))
    wf.close()


# Main application window
app = tk.Tk()
app.title("AGRINETCOM")

# Initial size of the window (width x height)
app.geometry("1200x700")

recording = False
frames_list = []

audio = pyaudio.PyAudio()
audio_stream = None

# Output
output_1 = "Welcome to a revolutionary world of agricultural transformation with KUDU Technologies! \n Our platform is the key to unlocking the true potential of agriculture by redefining the way supply chains operate.\n We are not just another technology provider; we are the pioneers of change in the agricultural industry. \n With us, you'll experience a spectacular journey that consolidates fragmented supply chains, embraces transparency, \n and empowers all stakeholders to thrive."
output_2 = "Kindly say the type of fruit you want, the source and how you want it delivered to you. \n Hit 'start speaking' to speak and press stop when done "

# Label widgets
label_1 = tk.Label(app, text=output_1, font=("Arial", 12))
label_1.grid(row=1, column=0, pady=10)

label_2 = tk.Label(app, text="What is your name? Press the button to SPEAK. Press STOP when done", font=("Verdana", 12))
label_2.grid(row=2, column=0, pady=10)

label_3 = tk.Label(app, text=output_2, font=("Arial", 12))
label_3.grid(row=5, column=0, pady=10)


# Button widgets
button_1 = tk.Button(app, text="SPEAK", command=start_recording)
button_1.grid(row=3, column=0, pady=10)

button_2 = tk.Button(app, text="STOP", command=stop_recording)
button_2.grid(row=4, column=0, pady=10)

button_3 = tk.Button(app, text="SPEAK", command=start_recording)
button_3.grid(row=6, column=0, pady=10)

button_4 = tk.Button(app, text="STOP", command=stop_recording)
button_4.grid(row=7, column=0, pady=10)

# Table widget
table_frame = ttk.Frame(app)
table_frame.grid(row=8, column=0, pady=10)

table = ttk.Treeview(table_frame, columns=("Column1", "Column2"), show="headings", height=3)
table.heading("Column1", text="Category")
table.heading("Column2", text="Choice")
table.insert("", "end", values=("Fruits", "Pineapple, Mango, Orange, Banana, Peach, Apple, Avocado, Watermelon, Grape"))
table.insert("", "end", values=("Source", "Online Suppliers, Specialty Stores, Homegrown, Seasonal Harvest, Fair Trade Certified, Sustainable Farms, Organic Farms, Local Farms"))
table.insert("", "end", values=("Delivery", "Home - delivery, Self - pickup"))
table.column("Column2", width= 600)  
table.pack()



# Start the main event loop
app.mainloop()