import os
import math
import numpy as np

import speech_recognition as sr
import pyautogui
import pvporcupine
import pyaudio
import wave
import librosa
import pickle

from sklearn.cluster import KMeans

CHUNK = 1024 
SAMPLE_FORMAT = pyaudio.paInt16 
CHANNELS = 1
RATE = 44100  
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "file.wav"

UP = "/media/tungthanhlee/data/uet6/xu ly tieng noi/assignment2/checkpoint/len.pkl"
RIGHT = "/media/tungthanhlee/data/uet6/xu ly tieng noi/assignment2/checkpoint/phai.pkl"
LEFT = "/media/tungthanhlee/data/uet6/xu ly tieng noi/assignment2/checkpoint/trai.pkl"
DOWN = "/media/tungthanhlee/data/uet6/xu ly tieng noi/assignment2/checkpoint/xuong.pkl"
def get_next_audio():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=SAMPLE_FORMAT,
        channels=CHANNELS,
        rate=RATE,
        frames_per_buffer=CHUNK,
        input=True,
    )

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    # while True:
        data = stream.read(CHUNK)
        frames.append(data)
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(SAMPLE_FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    # return frames

def get_mfcc(file_path):
    y, sr = librosa.load(file_path) # read .wav file
    hop_length = math.floor(sr*0.010) # 10ms hop
    win_length = math.floor(sr*0.025) # 25ms frame
    # mfcc is 12 x T matrix
    mfcc = librosa.feature.mfcc(
        y, sr, n_mfcc=12, n_fft=1024,
        hop_length=hop_length, win_length=win_length)
    # substract mean from mfcc --> normalize mfcc
    mfcc = mfcc - np.mean(mfcc, axis=1).reshape((-1,1)) 
    # delta feature 1st order and 2nd order
    delta1 = librosa.feature.delta(mfcc, order=1)
    delta2 = librosa.feature.delta(mfcc, order=2)
    # X is 36 x T
    X = np.concatenate([mfcc, delta1, delta2], axis=0) # O^r
    # return T x 36 (transpose of X)
    return X.T # hmmlearn use T x N matrix

def get_class_data(data_dir):
    # files = os.listdir(data_dir)
    # mfcc = [get_mfcc(os.path.join(data_dir,f)) for f in files if f.endswith(".wav")]
    mfcc = get_mfcc(data_dir)
    return mfcc

def clustering(X, n_clusters=14):
    kmeans = KMeans(n_clusters=n_clusters, n_init=100, random_state=0, verbose=0)
    kmeans.fit(X)
    print("centers", kmeans.cluster_centers_.shape)
    return kmeans 

if __name__ == '__main__':
    r = sr.Recognizer()

    while True:
        print("Say...")
        get_next_audio()
        direction = sr.WavFile(WAVE_OUTPUT_FILENAME)
        with direction as source:
            audio = r.record(source) 
        try:
            text = r.recognize_google(audio, language='en')
            print(text)
        except:
            print("I have no idea")
            pass



    # with open(UP, 'rb') as file:
    #     up = pickle.load(file)
    # with open(DOWN, 'rb') as file:
    #     down = pickle.load(file)
    # with open(RIGHT, 'rb') as file:
    #     right = pickle.load(file)
    # with open(LEFT, 'rb') as file:
    #     left = pickle.load(file)

    # models = {
    #     "len":up,
    #     "xuong":down,
    #     "trai":left,
    #     "phai":right,
    # }

    # while True:
    #     print("say a word")
    #     get_next_audio()
    #     audio = get_class_data(WAVE_OUTPUT_FILENAME)
    #     # print(audio)
    #     # vector = np.concatenate([np.concatenate(v, axis=0) for k, v in audio.items()], axis = 0)
    #     kmeans = clustering(audio)
    #     # print(kmeans)
    #     recordtest = list([kmeans.predict(v).reshape(-1,1) for v in [audio]])
        

    #     # print(len(audio))
    #     score = {cname : model.score(recordtest[0]) for cname, model in models.items()}
    #     # print(models['len'].score(recordtest))
    #     print(score)


        # if keyword_index==1:
        #     print(keyword_index)
        #     pyautogui.press('up')
        # if keyword_index==3:
        #     print(keyword_index)
        #     pyautogui.press('left')
        # if keyword_index==2:
        #     print(keyword_index)
        #     pyautogui.press('right')
        # if keyword_index==0:
        #     print(keyword_index)
        #     pyautogui.press('down')