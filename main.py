import json
import logging
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import googlesearch
import os
import smtplib
import speedtest
import re
import ctypes
import requests
from bs4 import BeautifulSoup
#from win32com import servers
import wolframalpha
import psutil
import sys
from Voice_Authentication import add_user, recognize, Remove_user

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
OWNER = "NIHAR"
chrome = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
tabUrl = "http://google.com/?#q="
Youtube = "https://www.youtube.com/results?search_query="
news = "https://inshorts.com/en/read"
WOLFRAMALPHA_API = "WR5G32-LE39LVT9XE"


def speak(text):
    engine.say(text)
    engine.runAndWait()


# speak("NIHAR IS GOOD BOY....")
speak("INITIALISING JARVIS....")


def wishMe():
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour <= 12:
        speak("GOOD MORNING! " + OWNER)
    elif 12 < hour <= 4:
        speak("GOOD AFTERNOON! " + OWNER)
    else:
        speak("GOOD EVENING" + OWNER)
    # speak("I AM AT YOUR COMMAND! HOW MAY I HELP YOU ?")


wishMe()


def takeCommand():
    global query
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("HOW MAY I HELP YOU ?")
        print("Listening... ")
        audio = r.listen(source, 4, 4)
    try:
        print("RECOGNISING....")
        query = r.recognize_google(audio)
        print(f"user SAID: {query}\n")
        query = query.lower()
    except Exception as e:
        print("SAY THAT AGAIN")
        takeCommand()
    return query


def print_headlines(response_text):
    soup = BeautifulSoup(response_text, 'lxml')
    headlines = soup.find_all(attrs={"itemprop": "headline"})
    for headline in headlines:
        print(headline.text)
        speak(headline.text)


def internet_availability():
    """
    Tells to the user is the internet is available or not.
    """
    try:
        _ = requests.get('http://www.google.com/', timeout=1)
        return "Yes, the internet connection is ok"
    except requests.ConnectionError as e:
        logging.error("No internet connection with message: {0}".format(e))
        return "No the internet is down for now"


def test_speed():
    servers = []
    threads = None
    s = speedtest.Speedtest()
    s.upload(pre_allocate=False)
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()
    results_dict = s.results.dict()
    download = results_dict.get('download')
    upload = results_dict.get('upload')
    ping = results_dict.get('ping')
    print('download speed = {0:.2f} MB per second upload speed = {1:.2f} MB per second ping= {2} '.format(
        download / 8000000, upload / 8000000, ping))
    speak('download speed = {0:.2f} MB per second upload speed = {1:.2f} MB per second ping= {2} '.format(
        download / 8000000, upload / 8000000, ping))


def get_location():
    try:
        send_url = "http://api.ipstack.com/check?access_key=" + "7635d86a7666d894e83c348db57838c3"
        geo_req = requests.get(send_url)
        geo_json = json.loads(geo_req.text)
        # print(geo_req.text)
        latitude = geo_json['latitude']
        longitude = geo_json['longitude']
        city = geo_json['city']
        state = geo_json['region_name']
        zipcode = geo_json['zip']
        speak("You are in {0}... and in {1} city and zip code is {2}".format(state, city, zipcode))
    except Exception as e:
        speak("Unable to get current location with error message: {0}".format(e))
        print(("Unable to get current location with error message: {0}".format(e)))


def Wolphram():
    client = wolframalpha.Client(WOLFRAMALPHA_API)
    if query.lower():
        try:
            if WOLFRAMALPHA_API:
                res = client.query(query.lower())
                speak(next(res.results).text)
                print(next(res.results).text)
                logging.debug('Successful response from Wolframalpha')
            else:
                speak("WolframAlpha API is not working.\n"
                      "You can get an API key from: https://developer.wolframalpha.com/portal/myapps/ ")
        except Exception as e:
            logging.debug('There is not answer with wolframalpha with error: {0}'.format(e))
            speak('Sorry, but I can not understand what do you want')


def System_Info():
    pid = os.getpid()
    # print(pid)
    py = psutil.Process(pid)
    # print(py)
    memory_use = py.memory_info()[0] / 2. ** 30
    # print(memory_use)
    speak("I use {0:.2f} GB..".format(memory_use))
    print("I use {0:.2f} GB..".format(memory_use))


flag = True
while flag:
    query = takeCommand()
    if query is None:
        speak("Object NULL please Speak again")
    elif 'wikipedia' in query.lower():
        speak("Searching Wikipedia..")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        print(results)
        speak(results)
    elif 'open youtube' in query.lower():
        webbrowser.get(chrome).open("youtube.com")
    elif 'open google' in query.lower():
        webbrowser.get(chrome).open("google.com")
    elif 'open' and '.com' in query.lower():
        regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
        url = re.search(regex, query)
        if url:
            # print(url.group())
            webbrowser.get(chrome).open(url.group())
        else:
            print("MATCH NOT FOUND PLEASE SPEAK AGAIN")
    elif 'search google' in query.lower():
        query = (query.replace("search google", ""))
        webbrowser.get(chrome).open(tabUrl + query, new=2)
    elif 'search youtube' in query.lower():
        query = (query.replace("search youtube", ""))
        print(query)
        webbrowser.get(chrome).open(Youtube + query, new=2)
    elif 'lock' in query.lower():
        speak('Sure sir')
        for value in ['pc', 'system', 'windows']:
            ctypes.windll.user32.LockWorkStation()
        speak('Your system is locked.')
    elif 'show news' in query.lower():
        response = requests.get(news)
        print_headlines(response.text)
    elif 'test speed' in query.lower():
        test_speed()
    elif 'check connection' in query.lower():
        speak(internet_availability())
    elif 'location' in query.lower():
        get_location()
    elif 'memory usage' in query.lower():
        System_Info()
    elif 'bye' in query.lower():
        speak("Bye... Bye.... Have A good day! ")
        flag = False
        sys.exit()
    elif 'thanks' in query.lower():
        speak("you're welcome!")
    elif 'how are you' in query.lower():
        speak("I am doing well!")
    elif 'hello' in query.lower():
        speak("Hi there!")
    elif 'add user' in query.lower():
        add_user()
    elif 'recognise' in query.lower():
        recognize()
    elif 'remove user' in query.lower():
        Remove_user()
    else:
        Wolphram()
