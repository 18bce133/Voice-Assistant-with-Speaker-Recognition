# import tensorflow as tf
import numpy as np
import os
import glob
import pickle
# import cv2
import time
import pyttsx3
import speech_recognition as sr1
import sys
import noisereduce
import matplotlib.pyplot as plt

# from numpy import genfromtxt
# from main import speak , takeCommand
# from keras import backend as K
# from keras.models import load_model

engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    global query
    r = sr1.Recognizer()
    with sr1.Microphone() as source:
        # speak("HOW MAY I HELP YOU ?")
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


# K.set_image_data_format('channels_first')
np.set_printoptions(threshold=sys.maxsize)

import pyaudio
from IPython.display import Audio, display, clear_output
import wave
from scipy.io.wavfile import read
from sklearn.mixture import GMM
import warnings

warnings.filterwarnings("ignore")

from sklearn import preprocessing
# for converting audio to mfcc
import python_speech_features as mfcc


def calculate_delta(array):
    """Calculate and returns the delta of given feature vector matrix"""

    rows, cols = array.shape
    deltas = np.zeros((rows, 20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i - j < 0:
                first = 0
            else:
                first = i - j
            if i + j > rows - 1:
                second = rows - 1
            else:
                second = i + j
            index.append((second, first))
            j += 1
        deltas[i] = (array[index[0][0]] - array[index[0][1]] + (2 * (array[index[1][0]] - array[index[1][1]]))) / 10
    return deltas


def extract_features(audio, rate):
    mfcc_feat = mfcc.mfcc(audio, rate, 0.025, 0.01, 20, appendEnergy=True, nfft=1103)
    mfcc_feat = preprocessing.scale(mfcc_feat)
    delta = calculate_delta(mfcc_feat)
    combined = np.hstack((mfcc_feat, delta))
    return combined

    # Voice authentication


def add_user():
    global source
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 3
    print("SAY THE NAME")
    speak("Say the name")
    name = takeCommand()
    source = 'D:/User Nihar/documents/HI/Jarvis/VOICE DATABASE/' + name
    # name = input("Enter Name:")
    if os.path.exists('D:/User Nihar/documents/HI/Jarvis/VOICE DATABASE/' + name):
        print("Name Already Exists! Try Another Name...")
        speak("Name Already Exists! Try Another Name...")
        exit(0)
    else:
        if os.path.exists("D:/User Nihar/documents/HI/Jarvis/VOICE DATABASE/"):
            source = "D:/User Nihar/documents/HI/Jarvis/VOICE DATABASE/" + name
            os.mkdir(source)
        else:
            source = "D:/User Nihar/documents/HI/Jarvis/VOICE DATABASE/"
            os.mkdir(source)
            source = "D:/User Nihar/documents/HI/Jarvis/VOICE DATABASE/" + name
            os.mkdir(source)

    for i in range(3):
        audio = pyaudio.PyAudio()

        if i == 0:
            j = 3
            while j >= 0:
                time.sleep(1.0)
                print("Speak your name in {} seconds".format(j))
                speak("Speak your name in {} seconds".format(j))
                clear_output(wait=True)

                j -= 1

        elif i == 1:
            print("Speak your name one more time")
            speak("Speak your name one more time")
            time.sleep(0.5)

        else:
            print("Speak your name one last time")
            speak("Speak your name one last time")
            time.sleep(0.5)

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        print("recording...")
        speak("recording...")

        frames = []

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # saving wav file of speaker
        waveFile = wave.open(source + '/' + str((i + 1)) + '.wav', 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        speak("Done")
        print("Done")

    dest = "D:/User Nihar/documents/HI/Jarvis/gmm_models/"
    count = 1

    for path in os.listdir(source):
        path = os.path.join(source, path)
        print(path)
        features = np.array([])

        # reading audio files of speaker
        (sr, audio) = read(path)

        # extract 40 dimensional MFCC & delta MFCC features
        vector = extract_features(audio, sr)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))

        # when features of 3 files of speaker are concatenated, then do model training
        if count == 3:
            gmm = GMM(covariance_type='diag', init_params='wmc', min_covar=0.001,
                      n_components=16, n_init=3, n_iter=200, params='wmc', random_state=None,
                      tol=0.001, verbose=0)
            gmm.fit(features)

            # saving the trained gaussian model
            pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
            print(name + ' added successfully')
            speak(name + ' added successfully')

            features = np.asarray(())
            count = 0
        count = count + 1

    # if __name__ == '__main__':
    #   add_user()
    ''' #import cPickle
        import numpy as np
        from scipy.io.wavfile import read
        from sklearn.mixture import GMM
        import warnings
        warnings.filterwarnings("ignore")

        # path to training data
        source = "development_set/"

        # path where training speakers will be saved
        dest = "D:/User Nihar/documents/HI/Jarvis/gmm_models/"
        train_file = "development_set_enroll.txt"
        file_paths = open(train_file, 'r')

        count = 1
        # Extracting features for each speaker (5 files per speakers)
        features = np.asarray(())
        for path in file_paths:
            path = path.strip()
            print(path)

            # read the audio
            sr, audio = read(source + path)

            # extract 40 dimensional MFCC & delta MFCC features
            vector = extract_features(audio, sr)

            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))
            # when features of 5 files of speaker are concatenated, then do model training
            if count == 5:
                gmm = GMM(n_components=16, n_iter=200, covariance_type='diag', n_init=3)
                gmm.fit(features)

                # dumping the trained gaussian model
                picklefile = path.split("-")[0] + ".gmm"
                pickle.dump(gmm, open(dest + picklefile, 'wb'))
                print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
                features = np.asarray(())
                count = 0
            count = count + 1
        '''


def recognize():
    # Voice Authentication
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    FILENAME = "D:/User Nihar/documents/HI/Jarvis/test.wav"

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("recording...")
    # speak("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")
    speak("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # saving wav file
    waveFile = wave.open(FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    modelpath = "D:/User Nihar/documents/HI/Jarvis/gmm_models/"

    gmm_files = [os.path.join(modelpath, fname) for fname in
                 os.listdir(modelpath) if fname.endswith('.gmm')]

    models = [pickle.load(open(fname, 'rb')) for fname in gmm_files]

    speakers = [fname.split("/")[-1].split('.gmm')[0] for fname
                in gmm_files]

    # read test file
    sr, audio = read(FILENAME)

    # extract mfcc features
    vector = extract_features(audio, sr)
    log_likelihood = np.zeros(len(models))

    # checking with each model one by one
    for i in range(len(models)):
        gmm = models[i]
        #print(gmm)
        scores = np.array(gmm.score(vector))
        #print(gmm.predict(vector))
        #print(gmm.predict_proba(vector))
        #print(scores)
        log_likelihood[i] = scores.sum()

    print("Likelihood: {}".format(log_likelihood))
    pred = np.argmax(log_likelihood)
    print("pred: {}".format(pred))
    identity = speakers[pred]

    # if voice not recognized than terminate the process
    if identity == 'unknown':
        print("Not Recognized! Try again...")
        speak("Not Recognized! Try again...")
        return

    print("Recognized as - ", identity)
    speak("Recognized as - {}".format(identity))
    ''' import os
       # import cPickle
        import numpy as np
        from scipy.io.wavfile import read
        #from speakerfeatures import extract_features
        import warnings
        warnings.filterwarnings("ignore")
        import time

        # path to training data
        source = "development_set\\"
        modelpath = "D:/User Nihar/documents/HI/Jarvis/gmm_models/"
        test_file = "development_set_test.txt"
        file_paths = open(test_file, 'r')

        gmm_files = [os.path.join(modelpath, fname) for fname in
                     os.listdir(modelpath) if fname.endswith('.gmm')]

        # Load the Gaussian gender Models
        models = [pickle.load(open(fname, 'rb')) for fname in gmm_files]
        speakers = [fname.split("\\")[-1].split(".gmm")[0] for fname
                    in gmm_files]

        # Read the test directory and get the list of test audio files
        for path in file_paths:

            path = path.strip()
            print(path)
            sr, audio = read(source + path)
            vector = extract_features(audio, sr)

            log_likelihood = np.zeros(len(models))

            for i in range(len(models)):
                gmm = models[i]  # checking with each model one by one
                scores = np.array(gmm.score(vector))
                log_likelihood[i] = scores.sum()
            print(log_likelihood)
            winner = np.argmax(log_likelihood)
            print("\tdetected as - ", speakers[winner])
            time.sleep(1.0)'''


def Remove_user():
    speak("Enter the name of the user")
    name = takeCommand()
    if os.path.exists('D:/User Nihar/documents/HI/Jarvis/VOICE DATABASE/' + name):
        [os.remove(path) for path in glob.glob('D:/User Nihar/documents/HI/Jarvis/VOICE DATABASE/' + name + '/*')]
        os.removedirs('D:/User Nihar/documents/HI/Jarvis/VOICE DATABASE/' + name)
        os.remove('D:/User Nihar/documents/HI/Jarvis/gmm_models/' + name + '.gmm')
        speak("The user removed Successfully")
    else:
        speak("The User Does not exists")
