#!/usr/bin/env python3
import os
from googleapiclient.discovery import build
from dhooks import Webhook

# Set this to the ID of whatever channel or playlist you want to check
id_to_check = "UUcmxOGYGF51T1XsqQLewGtQ"

# Set your YouTube API key and your discord channel hook as environment variables before you run
api_key = os.environ.get('YT_API_KEY')
hook_url = os.environ.get('DISCORD_CHANNEL_HOOK')

youtube = build('youtube', 'v3', developerKey=api_key)
hook = Webhook(hook_url)

request = youtube.playlistItems().list(
    part="snippet",
    playlistId=id_to_check
)

response = request.execute()

latest_video_title = response['items'][0]['snippet']['title']
latest_video_id = response['items'][0]['snippet']['resourceId']['videoId']

prev_id = ''

if os.path.exists('previous_latest.txt'):
    with open('previous_latest.txt', 'r') as prev:
        prev_id = prev.read()
    
if prev_id != latest_video_id:
    with open('previous_latest.txt', 'w') as prev:
        prev.write(latest_video_id)
        hook.send("New Episode Uploaded!\nLink: https://www.youtube.com/watch?v=" + latest_video_id)
