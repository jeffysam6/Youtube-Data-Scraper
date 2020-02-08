import json

import csv

import pandas as pd


from apiclient.discovery import build


api_key = "AIzaSyAT-sUvMTv6Y0IDHdpE22NzrQO_3FC5EJA"

youtube = build('youtube','v3',developerKey=api_key)

videoId = 'QCUwy_d-EPA'



req = youtube.commentThreads().list(
        part="snippet",
        maxResults=50,
        textFormat="plainText",
        videoId=videoId,
    )



res = req.execute()

comment_data = res['items']

#code for structured csv
with open('non_live_results2.csv','w') as f:
    writer = csv.writer(f,delimiter=',')

    writer.writerow(["Name","Comment","Likes"])

    for i in comment_data:

        each_comment = i['snippet']["topLevelComment"]["snippet"]

        writer.writerow([each_comment['authorDisplayName'],each_comment['textOriginal'],each_comment["likeCount"]])

        print(each_comment['authorDisplayName'],each_comment['textOriginal'],each_comment["likeCount"])




#unstructured csv
with open('non_live_data.json','w') as f:
        json.dump(comment_data,f)

df = pd.read_json('non_live_data.json')
    
df.to_csv("non_live_results.csv")







#Below code is to extract name and its corresponding comment.


# for c in comment_data:

    # print(c['snippet']['topLevelComment']['snippet']['authorDisplayName'],c['snippet']['topLevelComment']['snippet']['textDisplay'])


