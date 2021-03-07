import time
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os 
import json 
import random 
import webbrowser
import smtplib 
import twilio
import requests
import weather_forecast as wf 
import pyjokes
import wolframalpha
from urllib.request import urlopen 
import selenium 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import msvcrt as m


#import BeautifulSoup
from email.message import EmailMessage 
wolf_app_id = "AH8G86-95LHR4R8WV"

greeting_invocations = {
    'how are you': ['I am doing good, sir!','I hope it has been a good day, sir', 'Bonjour monsieur', 'I am well sir', 'At you service!' ],
     "What's up":  ['I am doing good, sir!','I hope it has been a good day, sir', 'Bonjour monsieur', 'I am well sir', 'At you service!' ],
     }
username = 'Nishanth'
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 145)
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
            if 'jarvis' in command:
                command = command.replace('jarvis','')
                print(command)
    except:
        engine.say("There seems to be a problem with your microphone!")
    return command.lower() 

#def run_alexa():
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

def start_greetings():
    time1 = int(datetime.datetime.now().hour)
    if time1 > 0 and time1 < 12: 
        talk('Good morning sir!')
    elif time1>= 12 and time1 < 18:
        talk('Good afternoon sir!')
    else:
        talk('Good evening sir!')

    talk('This is Jarvis, your virtual assistant')
    version = 'one point o'
    talk('Booting up ' + version)
    talk(" What can I do for you?")

# def make_calls():
# def tell_joke():
 
def send_email(receiver, subject, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('username', 'passwd')
    email = EmailMessage()
    email['From'] = 'username'
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(content)

def is_cancel(command):
    if command == 'cancel' or 'shutdown' or 'goodbye':
        exit()

def navigate(source, dest):
    driver = webdriver.Chrome('C:\\Users\\nisha\Downloads\\chromedriver_win32\\chromedriver')
   # url = 'https://www.google.com/maps'
    url = 'https://www.google.com/maps/dir///@41.7455503,-72.8585684,16z/data=!4m2!4m1!3e0'
    driver.get(url)
    source_field = driver.find_element_by_xpath('//*[@id="sb_ifc50"]/input')
    source_field.send_keys(source)
    dest_field = driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input')
    dest_field.send_keys(dest)
    dest_field.send_keys(Keys.RETURN)
    time.sleep(10)

#//*[@id="sb_ifc51"]/input
def wait():
    m.getch()

def main():
    start_greetings()
    
    while True:
        command = take_command() 
        # Playing youtube songs.....
        if 'play' in command:
            song = command.replace('play','')
            talk('Playing...' + song)
            pywhatkit.playonyt(song)

        # Searching up google results 
        elif 'search' in command:
            query = command.replace('search' , '')
            talk('Searching....'+ query)
            pywhatkit.search(query)
            #time.sleep(10)
            #is_cancel()

            main()


        #telling the time 
        elif 'time' in command:
            time1 = datetime.datetime.now().strftime("%I:%M %p")
            talk('Sir, it is currently '+ time1)
            time.sleep(5)
            continue 

        # Looking up wikipedia 
        elif 'look up' in command:
            query = command.replace('look up', '')
            resp = wikipedia.summary(query, 2)
            talk(resp)
            print(resp)
        
        #Sending an email
        elif 'email' in command:
            talk('Whom would you like to send an email to?')
            receiver = take_command()
            talk('Thank you, what would be the subject of you email')
            subject = take_command()
            talk('What would you like to write in your email')
            content = take_command()
            talk("Are your sure? Would you like to make any changes")
            resp = take_command()
            while 'no' in resp:
                talk('Please repeat your content, sir')
                content = take_command()
                talk('Are you satisfied with the contents of your email now sir?')
                resp = take_command()
                if 'yes' in resp:
                    send_email(receiver, subject, content)
                    break
                elif 'cancel' in resp:
                    main()

        elif 'browser' in command:
           # talk("Which site would you like to browse today?")
            #query = take_command()
            query = command.replace('browser', '')
            webbrowser.get('chrome').open(query)
            #webbrowser.open(query)

        elif 'weather' in command: 
            #talk('Please mention the place')
           # location = take_command()
            #query = 
            weather_api_key = 'd3a25fb22c54f3f1f5a6b19b2685190b'
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            talk("What city do you want the weather from?")
            city_name = take_command()
            print(city_name)
            final_url = base_url + "q="+ city_name + "&appid=" + weather_api_key
            response = requests.get(final_url)
            data = response.json()

            if data["cod"] != 404:
                main_data = data['main']
                current_temp = main_data['temp']
                curr_humidity = main_data['humidity']
                curr_descr = data['weather'][0]['description']
                print(current_temp)
                temp_celsius = current_temp - 273.15
                print(f'It is currently {temp_celsius} with humidity of {curr_humidity}. Weather descritption ....{curr_descr}')
                talk('It is currently' + str(temp_celsius)  + ' with humidity of ' + str(curr_humidity) + '. Weather description... '+ curr_descr)
            else:
                print("No weather data found")
                talk("No weather data found")


        #print(wf.forecast(place = "Bangalore" , time="23:15:00" , date="2019-09-12" , forecast="daily"))
        
        elif 'calculate' in command:
            
            client = wolframalpha.Client(wolf_app_id)
            indx = command.lower().split().index('calculate')
            command = command.split()[indx + 1:]
            res = client.query(' '.join(command))
            answer = next(res.results).text
            print("The answer is " + answer)
            talk("The answer is " + answer)

        elif 'where is' in command or 'what is the location of' in command:
            if 'where is' in command:
                command = command.replace('where is', '')
                print(command)
                print("$$$$$$$$$$$$")
            elif 'what is the location of' in command:
                command = command.replace('What is the location of', '')    
            print(command)
            location = command 
            print(location)
            talk('Locating....'+ location)
            webbrowser.open("https://www.google.com/maps/place/" + location + "")
            break    

        elif 'what is' in command or 'who is' in command:
            client = wolframalpha.Client(wolf_app_id)
            res = client.query(command) 

            try:
                print(next(res.results).text)
                talk(next(res.results).text)
                
            except StopIteration:
                print("No results found.")
                talk("No results found.")

            break

        elif 'joke' in command:
            print(pyjokes.get_joke())
            talk(pyjokes.get_joke())
            break

        elif 'news' in command: 
            try:
                news_api_key = 'a71a03f0a3c9406592636528e645357d'
                jsonObj = urlopen('''https://newsapi.org/v2/top-headlines?country=us&apiKey=a71a03f0a3c9406592636528e645357d''')
                data = json.load(jsonObj)

                talk('Here are some of the top news headlines from USA')
                print('Here are some of the top news headlines from USA')

                print('========================= Top Headlines ===================================')
                count = 1
                for news in data['articles']:
                    print(news['source']['name'])
                    print(news['title'])
                    print(news['description'])
                    talk("Headline number..."+ str(count))
                    talk("Source....." + news['source']['name'])
                    talk(" Article title.....")
                    time.sleep(3) 
                    talk(news['title'])
                    talk("Article description")
                    time.sleep(3) 
                    talk(news['description'])
                    count += 1
                    if count > 2:
                        talk('Should I continue?')
                        resp = take_command()
                        if 'yes' in resp:
                            count -= 2
                        elif 'no' in resp:
                            break

            except Exception as e:
                print(str(e))       

        elif 'navigate' in command:
            talk('Please tell me your place of origin')
            source = take_command()
            print(source)
            talk('Please tell me your destination')
            dest = take_command()
            print(dest)
            talk('navigating.......')
            navigate(source,dest)
            break
        elif 'music' in command:
            talk('What music would like to listen today?')
            music = take_command()
            print(music)
            talk('Searching....' + music)
            driver = webdriver.Chrome('C:\\Users\\nisha\Downloads\\chromedriver_win32\\chromedriver')
            search_bar = driver.find_element_by_xpath('//*[@id="input"]')
            search_bar.send_keys(music)
            search_bar.send_keys(Keys.RETURN)
            search_button = driver.find_element_by_xpath('//*[@id="contents"]/ytmusic-responsive-list-item-renderer')
            driver.execute_script("arguments[0].click();", search_button)



        
            
            #talk('The mode of transportation')
            
        #elif 'navigate' in command:
        

        # Integrate most regulary websites 

        # Amazon shopping bot  

if __name__ == '__main__':
    main()

    # Additional ideas for future implementation: 

        # Making managing phone calls 
        # if 'phone call' or 'call' in command:
        # Get the trending news 
        



