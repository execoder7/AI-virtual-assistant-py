import pyttsx3
import datetime
from soupsieve import select
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import time
import random
import pyjokes


# Defining dictionaries ========================

# The email feature will not work because the sender email field is empty 

emails = {
    'Receivers name':'email address'
    }
# Add path if running on a new pc
appPath = {
    'App name':'App path'
}

# Static - Values don't require any change
AIgreetings = ["I'm quite well", "I'm good, thank you for asking", "Pretty well", "All good", "Feeling quite electric"]

websites = {
    'youtube':'http://www.youtube.com',
    'google':'http://www.google.com',
    'stackoverflow':'http://www.stackoverflow.com',
    'facebook':'http://www.facebook.com',
    'twitter':'http://www.twitter.com',
    'instagram':'http://www.instagram.com',
    'messenger':'http://www.messenger.com',
    'whatsapp':'https://web.whatsapp.com/'
}




#  =====================CORE AI FUNCTION=====================
class coreAI():
    def __init__(self):
        # For getting voice
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id) 

    # Function for voice output
    def speak(self, audio):
        self.engine.say(audio)
        print(audio)
        self.engine.runAndWait()
        
    def takeCommand(self):
        self.r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            self.r.pause_threshold = 1
            self.r.energy_threshold = 300
            self.dynamic_energy_threshold = True
            self.dynamic_energy_adjustment_damping = 0.15
            self.dynamic_energy_ratio = 1.5

            self.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
            self.non_speaking_duration = 0.5  # seconds of non-speaking audio to keep on both sides of the recording

            self.audio = self.r.listen(source)

        try:
            print('Recognizing...')
            self.query = self.r.recognize_google(self.audio, language='en-US')
            print(f"User said: {self.query}\n")


        except Exception as e:
            # Displays error/exception
            # print(e)
            print("Say that again please..")
            return "None"
        return self.query




# =====================AI COMMANDS OPERATION=====================
class AICommands(coreAI):

    def __init__(self, command):
        super().__init__()

        # Greeting ==============================
        if 'how are you' in command:
            rand = random.randint(0, len(AIgreetings)-1)
            self.speak(AIgreetings[rand])

        elif 'what can you do' in command:
            self.speak('I can open various apps and websites, send an email, search a query, play some music or try to be funny')
            print('''
**************************
Note: the open apps, play music and send email features may not be unlocked if you are on a new pc.
Try adding path to the respected features.
**************************
''')
        # Online query search ==============================
        elif 'wikipedia' in command:
            self.speak('Searching Wikipedia...')
            self.query = command.replace('wikipedia,', '')
            self.results = wikipedia.summary(self.query, sentences=2)
            self.speak('According to Wikipedia')
            self.speak(self.results)

        elif 'search' in command:
            query = command.replace('search', '')
            self.speak('Searching Google...')
            webbrowser.open("https://www.google.com/search?client=firefox-b-d&q="+query)

        # Open websites ==============================
        elif 'open youtube' in command:
            path = websites.get('youtube')
            msg = 'Opening Youtube...'
            self.speak(msg)
            webbrowser.get('windows-default').open(path)

        elif 'open google' in command:
            path = websites.get('google')
            msg = 'Opening Google...'
            self.speak(msg)
            webbrowser.get('windows-default').open(path)

        elif 'open stack overflow' in command:
            path = websites.get('stackoverflow')
            msg = 'Opening stack overflow'
            self.speak(msg)
            webbrowser.get('windows-default').open(path)

        elif 'open facebook' in command:
            path = websites.get('facebook')
            self.speak('Opening facebook...')
            webbrowser.get('windows-default').open(path)

        elif 'open whatsapp web' in command:
            path = websites.get('whatsapp')
            self.speak('Opening WhatsApp Web...')
            webbrowser.get('windows-default').open(path)

        elif 'open instagram' in command:
            path = websites.get('instagram')
            self.speak('Opening Instagram...')
            webbrowser.get('windows-default').open(path)

        elif 'open twitter' in command:
            path = websites.get('twitter')
            self.speak('Opening Twitter...')
            webbrowser.get('windows-default').open(path)

        elif 'open messenger' in command:
            path = websites.get('messenger')
            self.speak('Opening Messenger...')
            webbrowser.get('windows-default').open(path)

        # Open applications ==============================
        # Add app paths above to unlock these features 

        # elif 'play music' in command or 'play some music' in command:
        #     music_dir = appPath.get('music')
        #     self.speak('Playing music')
        #     songs = os.listdir(music_dir)
        #     os.startfile(os.path.join(music_dir, songs[1]))

        # elif 'open firefox' in command or 'open the firefox' in command:
        #     path = appPath.get('firefox')
        #     self.speak('Opening firefox...')
        #     os.startfile(path)


        # elif 'open edge' in command or 'open the microsoft edge' in command or 'open the ms edge' in command or 'open ms edge' in command or 'open microsoft edge' in command:
        #     path = appPath.get('edge')
        #     self.speak('Opening microsoft edge...')
        #     os.startfile(path)

        # elif 'open chrome' in command:
        #     path = appPath.get('chrome')
        #     self.speak('Opening chrome...')
        #     os.startfile(path)

        # elif 'open vs code' in command or 'open the vs code' in command or 'open visual studio code' in command or 'open the visual studio code' in command:
        #     path = appPath.get('vscode')
        #     self.speak('Opening vs code...')
        #     os.startfile(path)

        # elif 'open ms word' in command or 'open word' in command or 'open microsoft word' in command:
        #     path = appPath.get('word')
        #     self.speak('Opening microsoft word...')
        #     os.startfile(path)

        # elif 'open excel' in command or 'open ms excel' in command or 'open microsoft excel' in command or 'open the ms excel' in command or 'open the microsoft excel' in command:
        #     path = appPath.get('excel')
        #     self.speak('Opening microsoft excel...')
        #     os.startfile(path)


        # Sending email ==============================
        
        
        elif 'send email' in command or 'send a email' in command or 'send mail' in command or 'send a mail' in command:
            try:
                self.speak('What should I send')
                self.content= input()
                self.speak('Whom should I send')
                self.to = input('Enter email: ')
                self.sendEmail(self.to, self.content)
                self.speak('Email has been sent!')

            except Exception as e:
                print(e)
                self.speak('Sorry, the email was not sent')

        
        # Joke ==============================
        elif 'joke' in command or 'something funny' in command:
            self.speak(pyjokes.get_joke())


        # For current time ==============================
        elif 'the time' in command or 'the current time' in command:
            strTime = datetime.datetime.now().strftime('%H:%M:%S')
            msg = (f'the current time is {strTime}')
            self.speak(msg)

        elif 'switch command type' in command or 'switch type' in command or 'change command type' in command:
            self.speak('Switching Command Type...')
            global selectType
            if selectType == '1':
                selectType = '2'
            else:
                selectType = '1'

        # To quit ==============================
        elif "shutdown" in command or 'turn off' in command or 'quit' in command or 'exit' in command:
            self.speak("Shutting down...")
            time.sleep(1)
            exit()

        


    # Send mail function
    def sendEmail(self, to, content):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login('malikshaiz09@gmail.com', 'pass=shaiz;') #Enter the sender email and password for the email feature
        self.server.sendmail('malikshaiz09@gmail.com', to, content) #Enter the sender email address
        self.server.close()

# Greet function
def greet():
    hour = int(datetime.datetime.now().hour)
    
    if hour >= 0 and hour <12:
        greeting = "Good Morning!"
        AI.speak(greeting)
    
    elif hour>=12 and hour<18:
        greeting = "Good Afternoon"
        AI.speak(greeting)

    else:
        greeting = "Good Evening" 
        AI.speak(greeting)

    AI.speak("I am LAIM 1.0, your virtual assistant.")




AI = coreAI()  
AIcommands = AICommands

global selectType

# ==================MAINLOOP==================
if __name__ == '__main__':
    greet()
    AI.speak('Please, select a command type')
    selectType = input("""
1) Command by voice
2) Command by typing

****************
Tip: You can switch between command types by commanding 'Switch type'
****************
>""")
    
    while True:

        if selectType == '1':
            print("""
****************
Tip: Try asking 'what can you do' 
****************""")
            while selectType == '1':
                
                query = AI.takeCommand().lower()
                # Logic for executing tasks base on query
                AIcommands(query)
                print('=========')

        elif selectType == '2':
            AI.speak('What would you like me to do?')
            print("""
****************
Tip: Try asking 'what can you do' 
****************""")
            while selectType == '2':
                query = input('''
===================
>''').lower()
                AIcommands(query)

        else:
            AI.speak('Invalid Input')
            exit()

