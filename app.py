# Import neccessary libraries
from flask import Flask, request, jsonify
from yt_helper import FetchVideos
import json
from utils import document
import argparse

parser = argparse.ArgumentParser(description='API key for Youtube Data v3 Service') # Pass new API key if required
parser.add_argument('--key', type=str, required=False, help='API key')

args = parser.parse_args()

api_key = ""

config = json.load(open("config.json"))
if(args.key is not None):
    api_key = args.key
else:
    api_key = config['API_KEY']


app = Flask(__name__)
fetch_service = FetchVideos(API_KEY=api_key)

def get_paginated_response(page):
    """
    Args:
        page (int): page number

    Returns:
        Payload: List of videos in the page requested 
    """
    # Create list of all videos
    videos = [] 
    for doc in document.find({}, {"_id": 0}):
        videos.append(doc)
    
    total_videos = len(videos)
    # return the section of videos for the request page by slicing the video list
    return json.dumps(videos[config['VIDEOS_PER_PAGE']*(page-1):config['VIDEOS_PER_PAGE']*(page)], indent = 4)
    

@app.route("/api/videos")
def get_video_from_title():
    desc = request.args.get('desc')
    title = request.args.get('search')
    page = request.args.get('page')

    # Check query params for the type of request
    if(title):
        video = document.find_one({"title": title}, {"_id" : 0})
        response = json.dumps(video, indent = 4)  
        return response
    elif(desc):
        video = document.find_one({"desc": desc}, {"_id" : 0})
        response = json.dumps(video, indent = 4)  
        return response
    elif(page):
        
        return get_paginated_response(int(page))

if __name__ == "__main__":
    app.run()
