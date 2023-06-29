import os

from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YouTube_API_KEY')

    def __init__(self, video_id):
        self.video_response = self.youtube().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                           id=video_id).execute()
        self.__video_id = video_id
        self.__video_title = self.video_response['items'][0]['snippet']['title']
        self.__video_url = f'https://www.youtube.com/watch?v={video_id}'
        self.__video_view_count = self.video_response['items'][0]['statistics']['viewCount']
        self.__video_like_count = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.__video_title}"

    @classmethod
    def youtube(cls):
        youtube = build('youtube', 'v3', developerKey=Video.api_key)
        return youtube


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__playlist_id = playlist_id