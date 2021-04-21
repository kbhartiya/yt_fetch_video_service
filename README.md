## Follow below steps to run the project

### Start a MongoDB server


> use yt_videos


> db.videos




In the Dockerfile replace <> after --key with the API key

Change the configuration in the config.json file


Run:

> docker build -t video_service


> docker run video_service


## Testing 

> GET http://127.0.0.1:5000/api/videos?page=< page-nummber >


> GET http://127.0.0.1:5000/api/videos?desc=< page-nummber >


> GET http://127.0.0.1:5000/api/videos?title=< page-nummber >
