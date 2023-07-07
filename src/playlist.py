import os
import datetime
import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YouTube_API_KEY')

    def __init__(self, playlist_id):
        self.playlist_info = self.youtube().playlists().list(part="snippet", id=playlist_id).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_info['items'][0]['id']
        self.__playlist_videos = self.youtube().playlistItems().list(playlistId=playlist_id,
                                                                   part='contentDetails',
                                                                   maxResults=50).execute()
        self.__playlist_id = playlist_id
        self.__video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.__playlist_videos['items']]
        self.__video_response = self.youtube().videos().list(part='contentDetails,statistics',
                                                      id=','.join(self.__video_ids)).execute()

    @property
    def total_duration(self):
        delta = datetime.timedelta()
        for video in self.__video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            delta += duration
        return delta

    def show_best_video(self):
        temp = []
        for video in self.__video_response['items']:
            temp.append(video['statistics']['likeCount'])
        temp_index = temp.index(max(temp))
        return f'https://youtu.be/{self.__video_response["items"][temp_index]["id"]}'

    @classmethod
    def youtube(cls):
        youtube = build('youtube', 'v3', developerKey=PlayList.api_key)
        return youtube