import json
import time
import pyautogui #automate GUI mouse
import pyttsx3 #text to speech
import requests # http request
import speech_recognition as sr #interface to speech api
import datetime #calculaton with date and time
import os
import cv2
from tkinter import scrolledtext
from requests import get
import wikipedia
import webbrowser
import urllib.parse #recognising the url
import pywhatkit as kit # sending whatsapp message
import tkinter as tk
from PIL import Image, ImageTk #image formats
from test import open_bluetooth_settings

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)
engine.setProperty('voice', voices[1].id)

class VirtualAssistantGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Virtual Assistant")
        self.root.geometry("745x360")
        self.root.resizable(0, 0)
        self.root.configure(bg='#D733FF')

        self.scrollable_text = scrolledtext.ScrolledText(self.root, state='disabled', height=15, width=87, relief='sunken', bd=5, wrap=tk.WORD, bg='#add8e6', fg='#800000')
        self.scrollable_text.place(x=10, y=10)

        mic_img = Image.open("ll.png")
        mic_img = mic_img.resize((55, 55), Image.ANTIALIAS)
        self.mic_img = ImageTk.PhotoImage(mic_img)

        self.listen_button = tk.Button(self.root, image=self.mic_img, borderwidth=0, activebackground='#2c4557', bg='#2c4557', command=self.launch_thread)
        self.listen_button.place(x=330, y=280)

        self.menu = tk.Menu(self.root)
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label='Commands List', command=self.commands_list)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

        self.menu.add_cascade(label="Clear Screen", command=self.clear_screen)

        self.root.config(menu=self.menu)

    def launch_thread(self):
        self.scrollable_text.configure(state='normal')
        self.scrollable_text.delete(1.0, tk.END)
        self.scrollable_text.insert(tk.END, self.get_greeting())
        self.scrollable_text.configure(state='disabled')
        self.scrollable_text.update()

        self.listen_button.configure(state='disabled')
        self.listen_button.update()

        self.scrollable_text.configure(state='normal')
        self.scrollable_text.insert(tk.END, "Listening...\n")
        self.scrollable_text.configure(state='disabled')
        self.scrollable_text.update()

        query = self.take_command()
        self.process_query(query)

        self.listen_button.configure(state='normal')
        self.listen_button.update()

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5)

        try:
            query = r.recognize_google(audio, language='en-in')
            self.scrollable_text.configure(state='normal')
            self.scrollable_text.insert(tk.END, f"User: {query}\n")
            self.scrollable_text.configure(state='disabled')
            self.scrollable_text.update()
            return query
        
        except Exception as e:
            print(e)
            self.scrollable_text.configure(state='normal')
            self.scrollable_text.insert(tk.END, f"Sorry, I didn't catch that. Please try again. Error: {str(e)}\n")
            self.scrollable_text.configure(state='disabled')
            self.scrollable_text.update()
            return ""

    def get_greeting(self):
        current_time = datetime.datetime.now()
        if 5 <= current_time.hour < 12:
            self.speak("Good morning mam! How may I help you?\n")
            return "Good morning! How may I help you?\n"
        elif 12 <= current_time.hour < 17:
            self.speak("Good afternoon mam! How may I help you?\n")
            return "Good afternoon! How may I help you?\n"
        else:
            self.speak("Good evening mam! How may I help you?\n")
            return "Good evening! How may I help you?\n"
    
    def process_query(self, query):
        if "open Notepad" in query:
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)
            self.speak("Opening Notepad")

        elif "open command prompt" in query:
            os.system("start cmd")
            self.speak("Opening Command Prompt")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()
            self.speak("Opening Camera")
        
        elif "open Bluetooth" in query:
            self.speak("Opening Bluetooth...")
            open_bluetooth_settings()

        elif "play music video" in query:
            music_dir="C:\\Users\\Kanishka\\Videos\\vdo_music"
            songs=os.listdir(music_dir)
            os.startfile(os.path.join(music_dir,songs[0]))

        elif "take a screenshot" in query:
            img_captured=pyautogui.screenshot()
            a=os.getcwd()
            if not os.path.exists("Screenshots"):
                os.mkdir("Screenshots")
            os.chdir(a+'\Screenshots')
            ImageName='screenshot-'+str(datetime.datetime.now()).replace(':','-')+'.png'
            img_captured.save(ImageName)
            os.startfile(ImageName)
            os.chdir(a)
            self.speak("Your screenshot is been saved to your screenshot folder.")

        elif "IP address" in query:
            ip=get("https://api.ipify.org").text
            self.speak(f"your IP address is {ip}")

        elif "Wikipedia" in query:
            self.speak("searching wikipedia....")
            query =query.replace("wikipedia","")
            results= wikipedia.summary(query,sentences=2)
            self.speak("according to wikipedia")
            self.speak(results)

        elif "open YouTube" in query:
            self.speak("opening youtube")
            webbrowser.open("www.youtube.com")

        elif "open telegram" in query:
            self.speak("opening telegram")
            webbrowser.open("https://telegram.org")

        elif "open stack overflow" in query:
            self.speak("opening stack overflow")
            webbrowser.open("https://stackoverflow.co")

        elif "open Google" in query:
            self.speak("What can i search for you?..")
            cm=self.take_command()
            cm=urllib.parse.quote(cm)
            webbrowser.open(f"https://www.google.com/search?q={cm}")

        elif "send a WhatsApp message" in query:
            self.speak("Please tell me the mobile number whom do you want to send message.")
            mobile_number=None
            while(True):
                mobile_number=self.take_command().replace(' ','')
                if mobile_number[0]=='0':
                    mobile_number=mobile_number[1:]
                if not mobile_number.isdigit() or len(mobile_number)!=10:
                    self.SR.speak("Please say it again")
                else:
                    break
            mobile_number.replace(' ','')
            self.speak("Tell me your message......")
            message=self.take_command()
            self.speak("Opening whatsapp web to send your message.")
            self.speak("Please be patient, sometimes it takes time.\nOR In some cases it does not works.")
            while(True):
                try:
                    kit.sendwhatmsg("+91"+mobile_number,message,datetime.datetime.now().hour,datetime.datetime.now().minute+1)
                    break
                except Exception:
                    pass
            time.sleep(20)
            self.speak('Message sent succesfully.')

        elif "today's news" in query:
            self.speak("Showing top 5 news of today.")
            r=requests.get('http://newsapi.org/v2/top-headlines?country=in&apiKey=a0fb760b87c64affa683d8e68a7a7051')
            data=json.loads(r.content)
            for i in range(5):
                news_title = data['articles'][i]['title']
                self.speak(news_title)
                self.scrollable_text.configure(state='normal')
                self.scrollable_text.insert('end', news_title + '\n')
                self.scrollable_text.configure(state='disabled')
                self.scrollable_text.see('end')
                self.scrollable_text.update()

        elif "play songs on YouTube" in query:
            self.speak("What song would you like to play?")
            song_name = self.take_command().lower()
            kit.playonyt(song_name)
        
        elif query == "ok good bye":
            self.speak("See you soon again bye bye.")
            self.root.destroy() 

        else:
            self.speak("Sorry, I didn't understand that command.")

    def speak(self, audio):
        self.scrollable_text.configure(state='normal')
        self.scrollable_text.insert(tk.END, f"Alexa: {audio}\n")
        self.scrollable_text.configure(state='disabled')
        self.scrollable_text.update()

        engine.say(audio)
        engine.runAndWait()

    def commands_list(self):
        self.scrollable_text.configure(state='normal')
        self.scrollable_text.insert(tk.END, "List of Commands:\n")
        self.scrollable_text.insert(tk.END, "- Open Notepad\n")
        self.scrollable_text.insert(tk.END, "- Open Command Prompt\n")
        self.scrollable_text.insert(tk.END, "- Open Camera\n")
        self.scrollable_text.insert(tk.END, "- Open Bluetooth\n")
        self.scrollable_text.insert(tk.END, "- Play music video\n")
        self.scrollable_text.insert(tk.END, "- take a screenshot\n")
        self.scrollable_text.insert(tk.END, "- IP address\n")
        self.scrollable_text.insert(tk.END, "- wikipedia\n")
        self.scrollable_text.insert(tk.END, "- Open youtube\n")
        self.scrollable_text.insert(tk.END, "- Open telegram\n")
        self.scrollable_text.insert(tk.END, "- Open stack overflow\n")
        self.scrollable_text.insert(tk.END, "- Open google\n")
        self.scrollable_text.insert(tk.END, "- Send a whatsapp message\n")
        self.scrollable_text.insert(tk.END, "- today's nws\n")
        self.scrollable_text.insert(tk.END, "- play songs on youtube\n")
        self.scrollable_text.insert(tk.END, "- ok good bye\n")
        self.scrollable_text.configure(state='disabled')
        self.scrollable_text.update()

    def clear_screen(self):
        self.scrollable_text.configure(state='normal')
        self.scrollable_text.delete(1.0, tk.END)
        self.scrollable_text.configure(state='disabled')
        self.scrollable_text.update()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    assistant_gui = VirtualAssistantGUI()
    assistant_gui.run()