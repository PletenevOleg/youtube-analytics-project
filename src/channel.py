import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YouTube_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__channel_id = self.channel["items"][0]["id"]
        self.__title = self.channel["items"][0]["snippet"]["title"]
        self.__description = self.channel["items"][0]["snippet"]["description"]
        self.__url = f"https://www.youtube.com/channel/{channel_id}]"
        self.__subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.__video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.__view_count = self.channel["items"][0]["statistics"]["viewCount"]

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def url(self):
        return self.__url

    @property
    def subscriber_count(self):
        return self.__subscriber_count

    @property
    def video_count(self):
        return self.__video_count

    @property
    def view_count(self):
        return self.__view_count

    def to_json(self, filename):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        dict_ = {
            "id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dict_, f)

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=Channel.api_key)
        return youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))