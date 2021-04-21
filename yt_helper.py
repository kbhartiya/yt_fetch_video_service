# Import necessary libraries
import time
from apiclient.discovery import build
from apiclient.errors import HttpError
from utils import document
import json
from video import Video
import threading


config = json.load(open("config.json"))

class FetchVideos():
    """Fetch Videos at a particular interval 
        and dump them in a mongo db collection 
    """
    def __init__(
        self, 
        API_KEY="", 
        search_query="cricket"
        ):
        """
        API key generated from google developers account
        Search query 

        Args:
            API_KEY (str, optional):
            search_query (str, optional): [description]. Defaults to "cricket".
        """
        self.api_key = API_KEY
        self.search_query = search_query
        self.youtube = build(config["API_SERVICE_NAME"], config["YOUTUBE_API_VERSION"], developerKey=self.api_key)
        self.db = document
        # Run the Fetch Video service on a separate thread
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
    
    def run(self):
        """
        Returns
        """
        token = None
        id = 0
        while(True):
            search_response = self.youtube.search().list(
                q=self.search_query,
                type="video",
                pageToken=token,
                order = "date",
                part="id,snippet",
                maxResults=10,
                location=None,
                locationRadius=None
            ).execute()

            # Stored all the videos in a list
            videos = []
            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                    video = Video(
                        search_result['snippet']['title'], 
                        search_result['snippet']['description'], 
                        search_result['snippet']['publishedAt'], 
                        search_result['snippet']['thumbnails']['default']['url']
                        )
                    videos.append(video.__dict__)
                    # Convert the video to dict in order to add it in the DB
                    self.db.insert_one(video.__dict__)
            try:
                nexttok = search_response["nextPageToken"]
                token = nexttok
            except Exception as e:
                token = "last_page"
            print("[Interval Id : {}] executed".format(id))
            id+=1
            time.sleep(10) # Wait for 10 seconds to make the next request
