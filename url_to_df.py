import os
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import pandas as pd
import numpy as np
import csv
import io
import re

def clean(youtube_url):

    api_key = "AIzaSyAYlcJkAwyshjEYK1acVSKgWWjOGmVp3l0"
    video_id = get_video_id(youtube_url)

    if not video_id:
        return "Invalid YouTube youtube_url"

    comments = scrape_youtube_comments(api_key, video_id)

    # Create a DataFrame from the comments
    df = pd.DataFrame({"Comments": comments})

    return df  # Modify the return value as needed


def get_video_id(youtube_url):
    parsed_url = urlparse(youtube_url)
    query_params = parse_qs(parsed_url.query)
    
    video_id = query_params.get('v')
    if video_id:
        return video_id[0]
    else:
        return None

def scrape_youtube_comments(api_key, video_id,max_results=500):
    # Set up the YouTube API client
    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    nextPageToken = None
    # Call the API to get comments
    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=min(max_results, 500),  # Max results per request (500 is the maximum allowed)
            pageToken=nextPageToken
        )
    
        response = request.execute()

        # Extract comments from the response
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
        nextPageToken = response.get('nextPageToken')

        if not nextPageToken or len(comments) >= max_results:
            break

    return comments



