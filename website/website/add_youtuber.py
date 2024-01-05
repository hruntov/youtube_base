from googleapiclient.discovery import build
from urllib.parse import urlparse, unquote
import os
API_KEY = os.environ.get('API_KEY')


class YoutubeApi:
    """A class to interact with the YouTube API."""

    def __init__(self, API_KEY, channel_url) -> None:
        self.API_KEY = API_KEY
        self.channel_url = channel_url
        self.username = None
        self.channel_id = None
        self.channel_title = None
        self.channel_description = None

    def get_username_from_url(self, channel_url: str) -> str:
        """
        Extract the username from the channel URL and return it.

        Parameters:
        channel_url (str): The URL of the YouTube channel.

        Returns:
        str: The username extracted from the channel URL.

        """
        parsed_url = urlparse(channel_url)
        if parsed_url.path.startswith("/channel/"):
            self.username = unquote(parsed_url.path[9:])
        elif parsed_url.path.startswith("/c/"):
            self.username = unquote(parsed_url.path[3:])
        elif parsed_url.path.startswith("/@"):
            self.username = unquote(parsed_url.path[2:])
        else:
            self.username = None
        return self.username

    def get_channel_data_from_username(self) -> dict:
        """
        Get the channel data from the username.

        This method first gets the username from the channel URL, then uses the YouTube API to get the channel data.
        It sets the channel_id, channel_title, and channel_description attributes of the YoutubeApi object based on the retrieved data.

        Returns:
        dict: The channel data retrieved from the YouTube API.

        """
        self.get_username_from_url(self.channel_url)
        if self.username:
            youtube = build('youtube', 'v3', developerKey=self.API_KEY)
            request = youtube.search().list(
                q=self.username,
                part="snippet",
                type="channel",
                maxResults=1
            )
            response = request.execute()
            if 'items' in response and response['items']:
                channel_data = response['items'][0]
                self.channel_id = channel_data['id']['channelId']
                self.channel_title = channel_data['snippet']['title']

                youtube = build('youtube', 'v3', developerKey=self.API_KEY)
                request = youtube.channels().list(
                    part="snippet",
                    id=self.channel_id
                )
                response = request.execute()
                if 'items' in response and response['items']:
                    self.channel_description = response['items'][0]['snippet']['description']

                return channel_data

            print("Url not correct.")


youtube1 = YoutubeApi(API_KEY, "https://www.youtube.com/channel/UCVp3HrjsHf13z4wdV6jDMyw")
youtube2 = YoutubeApi(API_KEY, "https://www.youtube.com/@teoriaihor")
youtube3 = YoutubeApi(API_KEY, "https://www.youtube.com/c/@EnglishClass101")

youtube1.get_channel_data_from_username()
youtube2.get_channel_data_from_username()
youtube3.get_channel_data_from_username()
