import speech_recognition as sr
import playsound
from gtts import gTTS
import os # for deleting audio files 
import pyjokes # for getting jokes
import wolframalpha # for calculations
import json 
import webbrowser # for opening webpages
import requests # for getting results from google answer boxes
from bs4 import BeautifulSoup # for parsing google answer boxes
# for getting time & date
from datetime import date
import datetime
import time 
from dotenv import load_dotenv

load_dotenv()
# Weather API
weather_key = os.getenv("weather_key")
base= "http://api.openweathermap.org/data/2.5/forecast?"

# Wolframalpha API
client_key = os.getenv("client_key")
client = wolframalpha.Client(client_key)

# For scraping google answer boxes
headers = {
  'User-Agent': 
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
params = {
  'hl': 'en'
}

def greetings():
  hour = int(datetime.datetime.now().hour)
  if hour>= 0 and hour<12:
    speak("Good Morning!")
  elif hour>= 12 and hour<18:
    speak("Good Afternoon")  
  else:
    speak("Good Evening")   
  speak("I am your voice Assistant Ada")

def command():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    #query = input() #(if you want to take written input)
    query = r.listen(source, phrase_time_limit = 20)
  try:
    print("Recognizing...")   
    query = r.recognize_google(query, language='en')
    return query
  except: 
    speak("Unable to Recognize your voice") 
    return "None"   

def speak(output):
  num=0
  print(output)
  num += 1
  response=gTTS(text=output, lang='en', tld='com.au')
  file = str(num)+".mp3"
  response.save(file)
  playsound.playsound(file, True)
  os.remove(file)

if __name__ == '__main__':
    clear = lambda: os.system('cls')
    greetings()
    while True:
      speak("How can I help you")
      query = command().lower()
      print(query)
      if "exit" in query or "bye" in query or "sleep" in query or "stop" in query:
        speak("Ok bye hope I helped")
        break
      if "calculate" in query or "who wrote" in query or "where is" in query:
            res = client.query(query)             
            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            except StopIteration:
                print ("No results found")
                speak("No results found")
      elif "open youtube" in query:
        speak("Opening Youtube\n")
        webbrowser.open("https://youtube.com")
      elif "open google" in query:
        speak("Opening Google\n")
        webbrowser.open("https://google.com")
      elif "open word" in query:
        speak("Opening Word\n")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\\Microsoft Office Word 2007.lnk')
      elif "open excel" in query:
        speak("Opening Word\n")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\\Microsoft Office Excel 2007.lnk')
      elif "open powerpoint" in query:
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\\Microsoft Office PowerPoint 2007.lnk')
      elif "who made you" in query or "who is your creator" in query or "who created you" in query:
        speak("I was made by Ananya Thomas")
      elif "tell me a joke" in query:
        speak(pyjokes.get_joke('en','all'))
      elif "how are you" in query:
        speak("I am fine")
      elif "what is the date" in query or "what is today's date" in query:
        speak(date.today())
      elif"what is the time" in query:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        speak(current_time)
      elif "what is the weather in" in query:
        query = query.split(" ")
        location =""
        for i in query[5:]:
          location = location + str(i) +" "
        print(location)
        url = base + "appid=" + weather_key + "&q=" + location 
        response = requests.get(url) 
        res = json.loads(response.text)
        print(res)
        if res["cod"] != "404": 
            weather = res['list'][0]['main']
            temp = round(weather['temp'] - 273.15)
            desc = res['list'][0]['weather'][0]['description']
            resp_string = "The temperature is " + str(temp) + " degree Celcius" + "\nPrediction for today is" + str(desc)
            speak(resp_string)
        else: 
            speak("City Not Found") 
      elif "news" in query or "headlines" in query:
        url = 'https://www.bbc.com/news'
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        headlines = soup.find('body').find_all('h3')
        i = 1
        headlines.pop(0)
        for headline in headlines:
          speak(headline.text)
          if(i==5):
              break
          i+=1
      elif "when did" in query or "when is" in query or "when was" in query:
        url = 'https://www.google.com/search?q='+query
        html = requests.get(url, headers=headers,params=params)
        soup = BeautifulSoup(html.text, 'html.parser')
        if soup.find('div', class_='Z0LcW') is not None:
          result = soup.find('div', class_='Z0LcW')
          speak(result.text)
        else:
          speak("No results found")
      elif "what is" in query or 'what are' in query or "who is" in query:
        url = 'https://www.google.com/search?q='+query
        html = requests.get(url, headers=headers,params=params)
        soup = BeautifulSoup(html.text, 'html.parser')
        if soup.find('div', class_='Z0LcW') is not None:
          answer = soup.find('div', class_='Z0LcW')
          speak(answer.text)
        if soup.find('div', class_='LGOjhe') is not None:
          snippet = soup.find('div', class_='LGOjhe')
          speak(snippet.text)
        elif soup.find('div', class_='di3YZe') is not None:
          answer = soup.find('div', class_='di3YZe')
          speak(answer.text)
        elif soup.find('div', class_='dAassd') is not None:
          i = 1
          for word in soup.find_all('div', class_='dAassd'):
            a=word.get_text()
            speak(a)
            if(i==5):
              break
            i+=1
        elif soup.find('span',class_='qv3Wpe') is not None:
          answer = soup.find('span', class_='qv3Wpe')
          speak(answer.text)
        if answer!=None or snippet!=None:
          continue
        else:
          speak("No results found")
      elif "songs similar to" in query or "song similar to" in query or "movies similar to" in query or "movies like" in query or "shows similar to" in query or "shows like" in query:
        url = 'https://www.google.com/search?q='+query
        html = requests.get(url, headers=headers,params=params)
        soup = BeautifulSoup(html.text, 'html.parser')
        if soup.find('div', class_='NJU16b') is not None:
          i = 1
          for word in soup.find_all('div', class_='NJU16b'):
            a=word.get_text()
            speak(a)
            if(i==5):
              break
            i+=1
        elif soup.find('div',class_='uoFCfc') is not None:
          i = 1
          for word in soup.find_all('div', class_='uoFCfc'):
            a=word.get_text()
            speak(a)
            if(i==5):
              break
            i+=1
        else:
          speak("No results found")
      elif "play the song" in query or "play" in query or "search youtube for" in query or "search on youtube" in query:
        songtosearch = ""
        if "play the song" in query or "search youtube for" or "search on youtube":
          query = query.split(" ")
          for i in query[3:]:
            songtosearch = songtosearch + str(i) +" "
        else:
          query = query.split(" ")
          for i in query[1:]:
            songtosearch = songtosearch + str(i) +" "
        song = "https://www.youtube.com/results?search_query=" + songtosearch
        webbrowser.open(song)
      else:
        speak("Sorry I do not understand the question")
