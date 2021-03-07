import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# engine.say("Hello! I am alexa")

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa','')
                print(command)
    except:
        pass
    return command 

def run_alexa():
    command = take_command()
    if 'play' in command:
        #talk('Playing...')
        song = command.replace('play','')
        talk('Playing...' + song)
        pywhatkit.playonyt(song)
    elif 'search' in command:
        query = command.replace('search' , '')
        talk('Searching....'+ query)
        pywhatkit.search(query)
    elif 'look up' in command:
        # query = command.split(" ")[-1]
        query = command.replace('look up' , '')
        print(query)
        info = wikipedia.summary(query,2)
        talk(info)
    else:
        talk('Please repeat your command!')
    # elif 'time' in command:
    #     time = datetime.datetime.now('%H %M')
    #     talk('It is ', time)



run_alexa()