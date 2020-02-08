import json

import csv

import pandas as pd


from apiclient.discovery import build


api_key = "AIzaSyAT-sUvMTv6Y0IDHdpE22NzrQO_3FC5EJA"

youtube = build('youtube','v3',developerKey=api_key)

videoId = 'QCUwy_d-EPA'



request = youtube.videos().list(
        part="statistics",
        id=videoId
    )

response = request.execute()

print(response)

vidInfo = response['items'][0]

# print(vidInfo['statistics']['viewCount'])

print(vidInfo['id'],vidInfo['statistics']['viewCount'],vidInfo['statistics']['likeCount'],vidInfo['statistics']['dislikeCount'],vidInfo['statistics']['commentCount'])


with open('yt_likes_dislikes.csv','w') as f:
    writer = csv.writer(f,delimiter=',')

    writer.writerow(["Video Id","Views","Likes","Dislikes","Comment Count"])

    writer.writerow([vidInfo['id'],vidInfo['statistics']['viewCount'],vidInfo['statistics']['likeCount'],vidInfo['statistics']['dislikeCount'],vidInfo['statistics']['commentCount']])

