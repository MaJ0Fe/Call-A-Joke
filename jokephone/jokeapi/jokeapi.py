# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 08:41:12 2024

@author: majo
"""

import requests
import json
import random
import datetime
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play


def get_joke():
    #API endpoint URL
    url = 'https://icanhazdadjoke.com/'
    #headers
    headers = {
        "Accept" : "application/json",
        "User-Agent" : "The Joke Phone (ferdinandvittorio@gmail.com) DEV"}

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print('Succes:', response.status_code)
            joke = response.json()['joke']
            print(joke)
            return joke
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def get_voices():
    api_key = "b4763af12c98486883b58018a8dc1170"
    user_id = "Lh2nqtt77qOEuZdCi1S0J1OGDTE2"
    #API endpoint URL
    url = 'https://api.play.ht/api/v2/voices'
    #headers
    headers = {
        "AUTHORIZATION" : api_key,
        "X-USER-ID" : user_id,
        "content-type" : "application/json"}

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print('Succes:', response.status_code)
            voices = response.json()
            return voices
        else:
            print('Error:', response.status_code)
            print(response.json()['error_message'])
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
def select_voice(voices):
    av_voices = []
    for v in voices:
        if v['voice_engine'] == "PlayHT2.0":
            av_voices.append({'name' : v['name'], 'id' : v['id']})
    sel_voice =  av_voices[random.randint(0, len(av_voices))]
    print("Selected Voice:", sel_voice['name'])
    return sel_voice['id']
    
def get_speach(text, voice):
    api_key = "b4763af12c98486883b58018a8dc1170"
    user_id = "Lh2nqtt77qOEuZdCi1S0J1OGDTE2"
    #API endpoint URL
    url = 'https://api.play.ht/api/v2/tts/stream'
    #headers
    headers = {
        "AUTHORIZATION" : api_key,
        "X-USER-ID" : user_id,
        "accept" : "audio/mpeg",
        "content-type" : "application/json"}
    
    data = {
        "text" : text,
        "voice" : voice,
        "output_format" : "mp3",
        "speed" : 0.1,
        "sample_rate" : 44100,
        "voice_engine" : "PlayHT2.0-turbo"}

    try:
        # Make a POST request to the API endpoint using requests.post()
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print('Succes:', response.status_code)
            audiobytes = response.content
            return audiobytes
        else:
            print('Error:', response.status_code)
            print(response.json()['error_message'])
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
def playback(audiostream):
    audio = AudioSegment.from_file(BytesIO(audiostream), format='mp3')
    audiofile = str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')) + "_output" + str(random.randint(100, 999)) + ".mp3"
    audio.export(audiofile, format='mp3')
    sound = AudioSegment.from_mp3(audiofile)
    play(sound)

def tell_joke(text, voice):
    audiostream = get_speach(text, voice)
    if audiostream:
        #print(audiostream)
        playback(audiostream)
    else:
        print('Failed to fetch Audiostream from API.')
        
def main():
    joke = get_joke()
    fallback_joke = "I hate perforated lines, they're tearable."
    voices = get_voices()
    
    voice = "s3://voice-cloning-zero-shot/e46b4027-b38d-4d24-b292-38fbca2be0ef/original/manifest.json" #fallback
    voice = select_voice(voices)

    if joke:
        tell_joke(joke, voice)
    else:
        print('Failed to fetch joke from API. Reverting to Fallback')
        tell_joke(fallback_joke, voice)

if __name__ == '__main__':
    main()
