from pymongo import MongoClient

from datetime import datetime

client = MongoClient()
db = client["yt_videos"]
document = db.videos
