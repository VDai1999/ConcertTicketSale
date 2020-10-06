# Import packages
import sys
import urllib.request, urllib.response, urllib.error
from bs4 import BeautifulSoup
import re
from apiclient.discovery import build
from oauth2client.tools import argparser
import pandas as pd

# Get statistics from YouTube
# Source: https://gist.github.com/lado936/ccaa3ba78deada0f9fcb041498535987
class SoupScrape:
    
    def GetStats(self, code):
        
        video_url = 'http://www.youtube.com/watch?v=' + code
        startpage = urllib.request.urlopen(video_url)
        soup = BeautifulSoup(startpage.read(), "lxml")
        
        # Get Number of Views
        rawview_data = soup.find('div', {'class': 'watch-view-count'})
        view_number = rawview_data.contents[0]
        view_number = re.sub('[^0-9]', '', view_number)
        
        # Get Number of Likes and Dislikes
        raw_like = soup.find('button', {'class': 'like-button-renderer-like-button'})
        raw_dislike = soup.find('button', {'class': 'like-button-renderer-dislike-button'})
        
        # Likes
        likes = raw_like.contents[0]
        for data in likes:
            num_of_likes = data

        # Dislikes
        dislikes = raw_dislike.contents[0]
        for data in dislikes:
            num_of_dislikes = data
            
        # Video name
        raw_name=soup.find('span', {'class': 'watch-title'})
        video_name=raw_name.contents[0]
        video_name=video_name.replace('\n', '')
        
         # Save this data in a dictionary 
        data = {'Video Name':video_name, 'Views':view_number, 'Likes':num_of_likes, 'Dislikes':num_of_dislikes} 
      
        # Return the dictionary 
        return data 
 
# Personal key to access YouTube API   
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Get Statistics for some music videos
if __name__ == "__main__":
   
    stat_fetch = SoupScrape()
    video_id = ["5Wiio4KoGe8","aJOTlE1K90k","SlPhMPnQ58k",
               "EBt_88nxG4c","J1OsKJW51HY","Z25aDKQ7Ojw",
               "2Vv-BfVoq4g","mj0XInqZMHY","ryJgDL9jzKk",
               "U9BwWKXjVaI","S1gp0m4B5p8","l0U7SxXHkPY"]
    stat_list = []
    for code in video_id:
        a = stat_fetch.GetStats(code)
        stat_list.append(a)

# Print out the statistics list        
print(stat_list)

# Change the dictionary to a dataframe
df=pd.DataFrame.from_dict(stat_list)

# Read the dataframe into a csv file
df.to_csv('VideoStat.csv', index=False)