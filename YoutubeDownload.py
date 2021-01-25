# Importing libraries 
import bs4 as bs 
from pytube import YouTube
import math
#from progressbar import ProgressBar
import threading

vidOrList = input("Enter (v) if you want to download a video or (p) if you want to download a playlist : ")

if(vidOrList == 'p'):
    import sys 
    import urllib.request 
    
    from PyQt5.QtWebEngineWidgets import QWebEnginePage 
    from PyQt5.QtWidgets import QApplication 
    from PyQt5.QtCore import QUrl 

    
    
    class Page(QWebEnginePage): 
        def __init__(self, url): 
            print("Please wait ...")
            self.app = QApplication(sys.argv) 
            QWebEnginePage.__init__(self) 
            self.html = '' 
            self.loadFinished.connect(self._on_load_finished) 
            self.load(QUrl(url)) 
            self.app.exec_() 
    
        def _on_load_finished(self): 
            self.html = self.toHtml(self.Callable) 
            print('Load finished') 
    
        def Callable(self, html_str): 
            self.html = html_str 
            self.app.quit() 
    
    
    playlist = [] 
    
    
    url = input("Enter the Youtube Playlist URL : ")
    # Scraping and extracting the video 
    # links from the given playlist url 
    page = Page(url) 
    soup = bs.BeautifulSoup(page.html, 'html.parser') 
    #print(soup.find_all('a',{"class":"ytd-playlist-video-renderer"}))
    dwType = input("Enter (a) if you want to download the whole playlist or (r) if you want to download videos in range or (i) if you want to download certain indices : ")
    firstVideo = 0
    lastVideo = 0
    indices = [] #array for indices

    if(dwType == 'r'): #if range is selected get first and last video
        firstVideo = input("Enter first video in range : ")
        lastVideo = input("Enter last video in range : ")

    check = 1 #check if x is selected to get out of the loop
    index = 0
    if(dwType == 'i'): # if indexs
        while (check):
            index = input("Enter index (x to stop) : ")
            if(index == 'x'):
                break
            indices.append(index)
        

    i = 1 #counter
    j = 0 #counter

    for links in soup.find_all('a',{"class":"ytd-playlist-video-renderer"}):
        
        link = links.get('href')
        if (link[0:6]=="/watch" and link[0]!="#"):
            link="https://www.youtube.com"+link
            link=str(link)
            if (dwType == 'r'):
                if (i >= int(firstVideo) and i <= int(lastVideo)):
                    playlist.append(link) 

            if(dwType == 'a'):
                playlist.append(link) 

            if(dwType == 'i'):
                if (i == int(indices[j])):
                    playlist.append(link) 
                    if(i == (int(indices[len(indices)- 1]))):
                        break
                    j += 1
        i += 1
        
    count = 1

    def progress_function(stream, chunk, bytes_remaining):
        print(round((1-bytes_remaining/video.filesize)*100, 3), '% done...',end = '\r')
    playlist = sorted(set(playlist), key = playlist.index)

    vquality = input("Enter the video quality (720,360):")
    vquality=vquality+"p"
    path = input("Enter the path : ")
    if(path == 'cse'):
        path = 'D:/Users/Rosser03/Downloads/Video/3rd computer'
    elif(path == 'video'):
        path = 'D:/Users/Rosser03/Downloads/Video'
        
    for link in playlist:
        try:
            yt = YouTube(link,on_progress_callback=progress_function) #get downloading links
            videos= yt.streams.filter(progressive=True,mime_type="video/mp4",res=vquality)
            video = videos[0]
            
        except:
            print("Video {number} failed to download . Download with other res ".format(number = count))
            try:
                if(vquality == '360p'): #change the quality and try again
                    vquality = '720p'
                else:
                    vquality = '360p'
                yt = YouTube(link)
                videos= yt.streams.filter(progressive=True,mime_type="video/mp4",res=vquality)
                video = videos[0]

            except:
                print("Exception occured. Either the video has no quality as set by you, or it is not available. Skipping video {number}".format(number = count))
                count += 1
                continue

        print('FileSize : ' + str(round(video.filesize/(1024*1024))) + 'MB')        
        print(yt.title + " - is downloading ...")
        video.download(path)
        print(yt.title + " - has been downloaded !!!")
        count += 1 

        """ 
            idea : get the failed videos and put it in an array and then download them again with the same res 
            if failed download another quality
        
        """

    

elif(vidOrList == 'v'):
    
    # Prints something like "15.555% done..." 
    def progress_function(stream, chunk, bytes_remaining):
        print(round((1-bytes_remaining/video.filesize)*100, 3), '% done...',end = '\r')

    
    url = input("Enter the Youtube Video URL :")
    yt = YouTube(url,on_progress_callback=progress_function)
    videoForSize = yt.streams.filter(progressive=True,mime_type="video/mp4")
    print('FileSize (360p) : ' + str(round(videoForSize[0].filesize/(1024*1024))) + 'MB')
    if( 1 < len(videoForSize) ):
        print('FileSize (720p) : ' + str(round(videoForSize[1].filesize/(1024*1024))) + 'MB')
    else:
        print('720p is not available')
           
    vquality = input("Enter the video quality (720,360):")
    vquality=vquality+"p"
    path = input("Enter the path : ")
    if(path == 'cse'):
        path = 'D:/CSE 3rd Videos'
    elif(path == 'co'):
        path = 'D:/CSE 3rd Videos/co'
    elif(path == 'sw'):
        path = 'D:/CSE 3rd Videos/sw'
    elif(path == 'dc'):
        path = 'D:/CSE 3rd Videos/dc'
    elif(path == 'pm'):
        path = 'D:/CSE 3rd Videos/pm'
    elif(path == 'control'):
        path = 'D:/CSE 3rd Video/control'
    elif(path == 'video'):
        path = 'C:/Users/ju/Downloads/Video'
    videos= yt.streams.filter(progressive=True,mime_type="video/mp4",res=vquality)
    video = videos[0]
    
    print(yt.title + " - is downloading ...")
    video.download(path)

    print(yt.title + " - has been downloaded !!!")
    



else:
    print("You have not enter (v) or (p)")
    exit()
