import sys
import re
from operator import itemgetter

import youtube_dl
import pydub
import eyed3

class Downloader:
    def __init__(self, url, path):
        self.url = url
        self.path = path
        
    def run(self):
        print('[1/3] Downloading the audio')
        self.download()
        print('[2/3] Dowloading metadata')
        track_list = self.get_tracklist()
        print('[3/3] Cutting and adding metadata')
        self.cut(track_list)
        print('DONE!')
        
    def get_tracklist(self):
        # download metadata
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
        with ydl:
            result = ydl.extract_info(
                self.url,
                download=False
            )

        # extracting tracklist from description:
        track_list = re.findall('(?P<datetime>\d+\:\d+)[ \|\:-]*(?P<artist>[^\-\:]*)[ -\:\|](?P<track>.*)', result['description'])
        for i, t in enumerate(track_list):
            arr = [0, 0, "", ""]
            datetime = t[0].split(":")
            arr[0] = int(datetime[0])*60 + int(datetime[1])
            arr[2] = t[1].strip()
            arr[3] = t[2].strip()
            track_list[i] = arr

        # adding end of track duration
        track_list.sort(key = itemgetter(0))
        for i in range(len(track_list)-1):
            track_list[i][1] = track_list[i+1][0]
        track_list[-1][1] = result['duration']
        
        return track_list
    
    def download(self):
        ydl = youtube_dl.YoutubeDL({
                "format": "bestaudio/best",
                "outtmpl": f"/tmp/%(id)s.%(ext)s",
                "ignoreerrors": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }
                ],
            }
        )
        
        with ydl:
            ydl.download([self.url])
            
    def cut(self, track_list):
        # load downloaded data
        filepath = f'/tmp/{self.url.split("v=")[-1]}.mp3'
        tracks = pydub.AudioSegment.from_mp3(filepath)
        
        for i, arr in enumerate(track_list):
            # cut the file
            file_name = arr[2] + ' - ' + arr[3] + '.mp3'
            tracks[arr[0]*1000:arr[1]*1000].export(self.path + '/' + file_name, format="mp3")
            
            # add metadata
            audiofile = eyed3.load(self.path + '/' + file_name)
            audiofile.tag.title = track_list[i][3]
            audiofile.tag.artist = track_list[i][2]
            audiofile.tag.save()
        
        
if __name__ == "__main__":
    if len(sys.argv) == 3:
        Downloader(sys.argv[1], sys.argv[2]).run()
    else:
        print("========================================")
        print("                 Playlisteo             ")
        print("========================================") 
        print("")
        print("USAGE : python playlisteo.py <URL> <Destination_folder>")
        print('Please type the full destination path')
