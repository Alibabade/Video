#from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit
#from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QProgressBar
#from PyQt5.QtWidgets import QRadioButton,QPlainTextEdit

"""
Download video/audio from Youtube 

Requirement:
1. PyQt5=5.15.2
2. Python >= 3.6
3. Pytube: pip install git+https://gitlab.com/obuilds/public/pytube@ob-v1
4. ffmpeg-python 

"""

from PyQt5.QtWidgets import *
import time
import sys
from pytube import YouTube
import ffmpeg
import os
import urllib.request
import re
import csv
    

class Yt_Downloader(QWidget):
    def __init__(self):
        super(Yt_Downloader, self).__init__()
        self.UI()

    def UI(self):

        # input youtube urls 
        self.label_urls = QLabel('Youtube Urls (support multiple urls):', self)
        self.label_urls.setGeometry(30,25,290,30)
        self.label_urls.setStyleSheet("color: rgba(200,201,217,255);")

        self.textbox = QPlainTextEdit(self)
        self.textbox.setGeometry(30,55, 400,100)
        self.textbox.setStyleSheet("background-color: rgba(25,27,50,255);\
                                    color: rgba(200,201,217,255);")

        # set downloading format
        self.radio_btn1 = QRadioButton('mp4',self)       
        self.radio_btn1.setChecked(True)
        self.download_format = 'mp4'
        self.radio_btn1.setGeometry(450,55, 80,20)
        self.radio_btn1.setStyleSheet("color: rgba(200,201,217,255);")
        self.radio_btn1.toggled.connect(lambda:self.radio_btn_state(self.radio_btn1))
        
        self.radio_btn2 = QRadioButton('mp3',self)
        self.radio_btn2.setGeometry(450,75, 80,20)
        self.radio_btn2.setStyleSheet("color: rgba(200,201,217,255);")
        self.radio_btn2.toggled.connect(lambda:self.radio_btn_state(self.radio_btn2))


        # set csv file path
        
        self.csv_browser_btn = QPushButton('Load .csv',self)
        self.csv_browser_btn.setGeometry(450,115, 80,30)
        self.csv_browser_btn.clicked.connect(self.browser_csv)
        self.csv_browser_btn.setStyleSheet("color: rgba(200,201,217,255);")

        # set saved path in local computer
        self.label_savepath = QLabel('Saved path',self)
        self.label_savepath.setGeometry(30,155,180,30)
        self.label_savepath.setStyleSheet("color: rgba(200,201,217,255);")

        self.savepath_text = QTextEdit(self)
        self.savepath_text.setGeometry(30, 185, 400,30)
        self.savepath_text.setStyleSheet("background-color: rgba(25,27,50,255);\
                                          color: rgba(200,201,217,255);")

        self.path_browser_btn = QPushButton('Choose Path', self)
        self.path_browser_btn.setGeometry(450, 185,100,30)
        self.path_browser_btn.clicked.connect(self.browser)
        self.path_browser_btn.setStyleSheet("color: rgba(200,201,217,255);")


        # set downloading progress bar
        self.label = QLabel('Downloading Progress', self)
        self.label.setGeometry(30,215,400,30)
        self.label.setStyleSheet("color: rgba(200,201,217,255);")

        self.p_bar = QProgressBar(self)
        self.p_bar.setGeometry(30,245,400,25)
        self.p_bar.setStyleSheet("background-color: rgba(31,94,138,255);")

        # button settings
        self.btn = QPushButton('Download', self)
        self.btn.setGeometry(450,245,80,25)
        self.btn.clicked.connect(self.Action)
        self.btn.setStyleSheet("color: rgba(200,201,217,255);")
                                
    

        self.btn_close = QPushButton('Close', self)
        self.btn_close.setGeometry(450, 310, 80,25)
        self.btn_close.clicked.connect(self.close)
        self.btn_close.setStyleSheet("color: rgba(200,201,217,255);")

        self.setStyleSheet("background-color: rgba(48,53,90,255);\
                            ")
        self.setGeometry(400,400,580,350)
        self.setWindowTitle("Youtube Downloader")
        self.show()

    def browser_csv(self):
        #options = QFileDialog.Options()
        self.csv_file  = QFileDialog.getOpenFileName(self, \
                                                       "Select a file",\
                                                       "",\
                                                       "CSV Files (*.csv)")
        if self.csv_file:
            print('csv file: ',self.csv_file[0])
        
        with open(self.csv_file[0], 'r') as f:
            for row in csv.reader(f):                
                print(row[0])
                self.textbox.insertPlainText(row[0]+'\n') 


    def browser(self):
        self.download_path = str(QFileDialog.getExistingDirectory(self, 'Select Directory'))
        self.savepath_text.setText(self.download_path)

    def radio_btn_state(self, radio_btn):
        if radio_btn.text() == 'mp4':
            self.download_format = 'mp4'
        elif radio_btn.text() == 'mp3':
            self.download_format = 'mp3'

    # return the itag of the highest resolution of stream object
    def get_highest_resolution(self, stream):
        # input argument: stream is a list
        res = 360; itag = None #; progressive=False
        for i in range(len(stream)):
            #print('stream[i]: ', stream[i])
            res_stm = int(stream[i].resolution[:-1]) if stream[i].resolution is not None else 0
            if res <= res_stm:
                res = res_stm
                itag = stream[i].itag
                #progressive = stream[i].progressive
        return itag




    def Action(self):

        textValues = self.textbox.toPlainText()
        urls = textValues.split('\n')
        if '' in urls:
            urls.remove('')
        for i,url in enumerate(urls,start=1):
            #print('url: ',url)
          #if re.match("^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$", url):  
            yt = YouTube(url)
            #print('streams: ', yt.streams.all())
            if self.download_format == 'mp3': 
                #audio = yt.streams.filter(only_audio=True).first()
                stm = yt.streams.get_audio_only()
                
                audio = yt.streams.get_by_itag(stm.itag)
                audio_saved = audio.download(self.download_path)
                
                os.rename(audio_saved, audio_saved[:-4]+'.mp3')

            # default to download the highest resolution videos
            elif self.download_format == 'mp4':
               
                stm = yt.streams.filter(file_extension='mp4').all()
                #print('stm : ', stm)
                itag = self.get_highest_resolution(stm)
                #print('itag: ', itag)
                video = yt.streams.get_by_itag(itag)
                #print('video title: ', video.title) 
                video_path = video.download(self.download_path)
                video_renamed_path = video_path[:-4] + '_video.mp4'
                os.rename(video_path, video_renamed_path)
                #print('is_progressive: ', video.is_progressive)
                if not video.is_progressive:
                    audio = yt.streams.filter(file_extension='mp4', only_audio=True).first()
                    #print('audio: ',audio)                                   
                    audio_path = audio.download(self.download_path)
                    #print('audio title: ', audio_path) 
                    audio_renamed_path = audio_path[:-4]+'_audio.mp4'
                    os.rename(audio_path, audio_renamed_path)
                    #merge two stream object file into one video file
                    video_stream = ffmpeg.input(video_renamed_path)
                    audio_stream = ffmpeg.input(audio_renamed_path)
                    ffmpeg.output(audio_stream, video_stream, video_path[:-4] + '_merged.mp4', strict=-2).run()    
                
            self.p_bar.setValue(i/len(urls)*100)

def main():

    app = QApplication([])

    window = Yt_Downloader()
    
    sys.exit(app.exec_())

if __name__ == "__main__":

    main() 
