import json

import csv

import pandas as pd

import requests


from apiclient.discovery import build


api_key = ""#youtube api key               




def generate_access_token():
    api_endpoint = "https://www.googleapis.com/oauth2/v4/token"

    refresh_token = ""

    client_id = ""

    client_secret = ""

    data = {'refresh_token':refresh_token, 
        'client_id':client_id, 
        'client_secret':client_secret,
        'grant_type':"refresh_token",
        'redirect_uri':"http://localhost"
        }

    headers_for_access_token = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    r = requests.post(url =api_endpoint, data = data,headers=headers_for_access_token) 

    return r.json()["access_token"]


access_token = generate_access_token()


# request = youtube.liveBroadcasts().list(
#         part="snippet",
#         broadcastType="all",
#         mine=True,
#     )


#headers required while calling the api
headers = {
  'Authorization': 'Bearer ' +  access_token,
  'Content-Type': 'application/json; UTF-8',
}


#first request to retrieve all the live stream which are stored in an array
r=requests.get(f"https://www.googleapis.com/youtube/v3/liveBroadcasts?part=snippet&broadcastType=all&mine=true&key={api_key}", headers=headers)


# response = request.execute()

# print(response)


# print(r.json())

title = r.json()['items'][0]['snippet']['title']

title = title.split("|")[0]

start_time = r.json()['items'][0]['snippet']['scheduledStartTime'].split('T')[1][:-1]



#current or latest live stream will be at the front of the array
liveChatId = r.json()['items'][0]['snippet']['liveChatId']
print("Start time ",start_time)
print("Live chat id",liveChatId)


#Second request to get comments by passing the livechatid
r2=requests.get(f"https://www.googleapis.com/youtube/v3/liveChat/messages?liveChatId={liveChatId}&part=snippet&key={api_key}", headers=headers)

# print(r2.json()['items'][0])
# print(r2.json())

comment_data = r2.json()['items']



#function to extract username from channel id
def username(channel_id):

    req = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={api_key}",headers=headers)

    return req.json()['items'][0]['snippet']['title']



#code to add data into csv
with open('live_results2.csv','w') as f:
    writer = csv.writer(f,delimiter=',')

    writer.writerow(["Youtube Session ID","Youtube Comment ID","Youtube Comment Content","Youtube Comment By","Youtube Comment Date & Time"])

    for i in comment_data:

        comment_time = i['snippet']['publishedAt'].split('T')[1][:-1]

        writer.writerow([title,i['id'],i['snippet']['displayMessage'],username(i['snippet']['authorChannelId']),comment_time])

        # print(title,i['id'],i['snippet']['displayMessage'],username(i['snippet']['authorChannelId']),i['snippet']['publishedAt'])




#dumping the same data in json file
with open('live_data.json','w') as f:
        json.dump(comment_data,f)

# df = pd.read_json('live_data.json')
    
# df.to_csv("live_results.csv")

