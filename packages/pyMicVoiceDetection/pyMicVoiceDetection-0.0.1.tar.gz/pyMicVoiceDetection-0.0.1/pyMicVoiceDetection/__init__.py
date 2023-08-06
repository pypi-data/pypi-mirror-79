#!/usr/bin/env python
# coding: utf-8
import wave
import pyaudio
from pyaudio import PyAudio,paInt16
import sys
import time
import numpy as np
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
sampwidth=2
def save_wave_file(filename,data):
    '''save the data to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(sampwidth)
    wf.setframerate(RATE)
    wf.writeframes(b"".join(data))
    wf.close()
    
def Record(filename,buf,dur=3):
    pa=PyAudio()
    stream=pa.open(format = FORMAT,channels=CHANNELS,
    rate=RATE,input=True,
    frames_per_buffer=CHUNK)
    count=0
    try:
        while count<dur*RATE/CHUNK :#控制錄音時間 #
            string_audio_data = stream.read(CHUNK,exception_on_overflow = False)#一次性錄音取樣位元組大小
            buf.append(string_audio_data)
            count+=1
            print('.',end='')
    finally:stream.close()
    save_wave_file(filename,buf)

def play_wav(wav_filename, chunk_size):
    try:
        print('Trying to play file ' + wav_filename)
        wf = wave.open(wav_filename, 'rb')
    except IOError as ioe:
        sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
        str(ioe) + '. Skipping.\n')
        return
    except EOFError as eofe:
        sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
        str(eofe) + '. Skipping.\n')
        return
    # Instantiate PyAudio.
    p = pyaudio.PyAudio()
    # Open stream.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),output=True)
    data = wf.readframes(chunk_size)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk_size)

def _rms(x):
    return np.sqrt(x.dot(x)/x.size)

def recordAsyn(filename,RECORD_SECONDS=25,TH=0.01,retSamples=None):
    #WAVE_OUTPUT_FILENAME = "output.wav"
    _MAX_VALUE=np.iinfo(np.int16).max    
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    print("* recording...")
    energy = [];    buf=[]
    S='silence'
    serial = 0;    silenceNum=0;    waitNum=0
    iterationPerSec = int(RATE/CHUNK)
    HALF_CHUNK = int(CHUNK/2)
    for i in range(0, RECORD_SECONDS*iterationPerSec):
        #若每個frame 512個samples，一個frame:512/16000=32ms
        data = stream.read(CHUNK, exception_on_overflow = False)
        sample=np.frombuffer(data,np.int16)/_MAX_VALUE
        e1=_rms(sample[0:HALF_CHUNK])
        e2=_rms(sample[HALF_CHUNK:CHUNK])
        energy.append(e1)
        energy.append(e2)
        if S=='silence':
            if e1>TH and e2>TH:
                buf.append(data)
                S='voice'
        elif S=='voice':
            buf.append(data)
            if e1<TH and e2<TH:
                silenceNum+=1
                if silenceNum>5:
                    serial+=1
                    save_wave_file(filename,buf)
                    print(filename + ".......saved")
                    break
            else: silenceNum=0
            
        if retSamples != None: retSamples.extend(list(sample))
        
    stream.close()
    p.terminate()
    
def recordAsynSerial(RECORD_SECONDS=25,TH=0.01,label="",retSamples=None):
    #WAVE_OUTPUT_FILENAME = "output.wav"
    _MAX_VALUE=np.iinfo(np.int16).max    
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    print("* recording...")
    energy = [];    buf=[]
    S='silence'
    startTime = time.strftime("%Y%m%d_%H%M%S", time.localtime()) 
    serial = 0;    silenceNum=0;    waitNum=0
    iterationPerSec = int(RATE/CHUNK)
    HALF_CHUNK = int(CHUNK/2)
    for i in range(0, RECORD_SECONDS*iterationPerSec):
        #若每個frame 512個samples，一個frame:512/16000=32ms
        data = stream.read(CHUNK, exception_on_overflow = False)
        sample=np.frombuffer(data,np.int16)/_MAX_VALUE
        e1=rms(sample[0:HALF_CHUNK])
        e2=rms(sample[HALF_CHUNK:CHUNK])
        energy.append(e1)
        energy.append(e2)
        if S=='silence':
            if e1>TH and e2>TH:
                buf.append(data)
                S='voice'
        elif S=='voice':
            buf.append(data)
            if e1<TH and e2<TH:
                silenceNum+=1
                if silenceNum>5:
                    serial+=1
                    filename = label + '_' +startTime +"_"+str(serial)+".wav"
                    save_wave_file(filename,buf)
                    #y, sr = librosa.load(filename,sr=None)
                    avgLL = LL/len(data)
                    print(avgLL)
                    print(filename + ".......saved")
                    buf=[]
                    S='wait'
                    silenceNum=0
            else: silenceNum=0        
        elif S=='wait':  
            waitNum+=1
            if waitNum>iterationPerSec*1:
                S='silence'
        if retSamples !=None : retSamples.extend(list(sample))

    stream.close()
    p.terminate()


