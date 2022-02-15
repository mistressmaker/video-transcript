#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 10:52:13 2022

@author: brookeweborg
"""

import speech_recognition as sr
import subprocess
import os
import argparse
from pymediainfo import MediaInfo as mi

def convert_video_to_audio_ffmpeg(video_file, output_ext="WAV"):
    #https://www.thepythoncode.com/article/extract-audio-from-video-in-python
    """Converts video to audio directly using `ffmpeg` command
    with the help of subprocess module"""
    filename, ext = os.path.splitext(video_file)
    splitFile = filename.split('/')
    filename = splitFile[-1]
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return filename + '.' + output_ext

def main():
    #Take in a file
    parser = argparse.ArgumentParser()
    parser.add_argument('FilePath', metavar='F', type=str, nargs=1,
                        help='the file to be transcripted')
    args = parser.parse_args()
    myPath = os.path.normpath(args.FilePath[0])
    
    fileInfo = mi.parse(myPath)
    videoFlag = False
    for track in fileInfo.tracks:
        if track.track_type == "Video":
            newFile = convert_video_to_audio_ffmpeg(myPath)
            videoFlag = True
            
    if not(videoFlag):
            newFile = myPath
            
    
    r = sr.Recognizer()
    
    with sr.AudioFile(newFile) as source:
        audioText = r.listen(source)
        
        try:
            print('Converting audio to text...')
            text = r.recognize_google(audioText)
            text_file = open("output.txt", "w")
            text_file.write(text)
            text_file.close()
            
        except Exception as e:
            print('Error', e)
        
if __name__ == "__main__":
    main()