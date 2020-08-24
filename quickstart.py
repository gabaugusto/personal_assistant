from __future__ import print_function
import pickle
import pyttsx3 # pip install pyttsx3
import datetime
import time
import speech_recognition as sr # pip install SpeechRecognition
import wikipedia # pip install wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui # pip install pyautogui
import psutil # pip install psutil
import pyjokes # pip install pyjokes

from selenium import webdriver #pip install selenium 
from selenium.webdriver.common.keys import Keys


#Definitions
person = "Carla"
term = "Paracoccidioides brasiliensis"    

#driver 
driver = webdriver.Firefox(executable_path=r"C:/projects/Python/source/firefoxdriver/geckodriver.exe")
driver.get('https://www.ncbi.nlm.nih.gov/')
data_dir = os.path.expanduser('C:/Users/Estevam-NB/Desktop/Python/export/printscreens/')
screen_dir = os.path.expanduser('C:/Users/Estevam-NB/Desktop/Python/export/printscreens/')
article_dir = os.path.expanduser('C:/Users/Estevam-NB/Desktop/Python/export/printscreens/')

# GMail: If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

#Voices
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[len(voices)-3].id)

def speak(audio):
    """Main function to vocalize
    """    
    engine.say(audio)
    engine.runAndWait()
 
def time():
    """Get and say current time
    """       
    Time = datetime.datetime.now().strftime("%I:%M:%S") 
    speak("Hora: ")
    speak(Time)

def date():
    """Get and say current date
    """       
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak(day)
    speak("de")
    speak(month)
    speak("de")
    speak(year)

def wishme():
    """Greetings
    """       
    speak("Welcome back sir!")
    time()
    date()
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour<12:
        speak("Good morning,")
        speak(person)
    elif hour >=12 and hour<18:
        speak("Good afternoon,")
        speak(person)
    elif hour >= 18 and hour<24:
        speak("Good evening,")
        speak(person)
    else:
        speak("Good night,")
        speak(person)

    speak("Buzzy at your service. Please tell me how can i help you?")

def sendEmail(to, content):
    """Simple sending e-mails
    """       
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('gab.augusto@gmail.com', '123')
    server.sendmail('gab.augusto@gmail.com', to, content)
    server.close()

def screenshot():
    """Taking Screenshots
    """       
    img = pyautogui.screenshot()
    img.save(screen_dir)

def cpu():
    """CPU Analizes
    """   
    usage = str(psutil.cpu_percent())
    speak('CPU is at'+ usage)
    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(battery.percent )

def jokes():
    """Everyone should smile sometimes :)
    """   
    speak(pyjokes.get_joke())              

def takeCommand():
    """Listening function. 
       Listen, Recognize or say an error
    """       
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recongnizning...")
        query = r.recognize_google(audio, language='en-in')
        print(query)

    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "None"
    return query 

def lookUpForArticles(term):
    """Lookup for articles 
    """         
    if not os.path.exists(screen_dir):
        os.makedirs(screen_dir)

    while True:
        searchbutton = driver.find_element_by_id('search')
        searchbar = driver.find_element_by_id('term')
        searchbar.send_keys(term)
        searchbar.send_keys(Keys.ENTER)        
        searchbutton.click()
        time.sleep(5)
        driver.quit()
                 
if __name__ == "__main__":
	wishme()
	
	while True:

		query = takeCommand().lower()
		if 'time' in query:
			time()
   
		elif 'date' in query:
			date()
   
		elif 'wikipedia' in query:
			speak("Searching...")
			query = query.replace("wikipedia","")
			result = wikipedia.summary(query, sentences=2)
			print(result)
			speak(result)
   
		elif 'send email' in query:
			try:
				speak("What should I say?")
				content = takeCommand()
				to = 'gabriel@gmail.com'
				sendEmail(to,content)
				speak("Email has been sent!")
			except Exception as e:
				print(e)
				speak("Unable to send the email")

		elif 'search in chrome' in query:
			speak("What should i search ?")
			chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
			search = takeCommand().lower()
			wb.get(chromepath).open_new_tab(search+'.com')
		
		elif 'logout' in query:
			os.system("shutdown -l")

		elif 'shutdown' in query:
			os.system("shutdown /s /t 1")

		elif 'restart' in query:
			os.system("shutdown /r /t 1")
		
		elif 'play songs' in query:
			songs_dir = 'D:\\Music'
			songs = os.listdir(songs_dir)
			os.startfile(os.path.join(songs_dir, songs[0]))

		elif 'remember that' in query:
			speak("What should I remember?")
			data = takeCommand()
			speak("you said me to remember that"+data)
			remember = open('data.txt','w')
			remember.write(data)
			remember.close()
			
		elif 'do you know anything' in query:
			remember =open('data.txt', 'r')
			speak("you said me to remember that" +remember.read())

		elif 'articles' in query:
			lookUpForArticles(term)
			speak("Done!")

		elif 'screenshot' in query:
			screenshot()
			speak("Done!")

		elif 'cpu'in query:
			cpu()

		elif 'joke' in query:
			jokes()

		elif 'offline' in query:
			quit()