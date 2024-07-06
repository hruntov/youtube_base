import os
from urllib.parse import unquote, urlparse

from dotenv import load_dotenv
from googleapiclient.discovery import build


class YoutubeApi:
    """A class to interact with the YouTube API."""

    #: (str): The URL of the YouTube channel.
    channel_url = ''

    #: (str): The custom name of the channel.
    channel_username = ''

    #: (str): The identifier of the channel.
    channel_id = ''

    #: (str): The title of the channel.
    channel_title = ''

    #: (str): The full description of the channel.
    channel_description = ''

    def __init__(self, channel_url) -> None:
        load_dotenv()
        self.__api_key = os.environ.get('API_KEY')
        self.channel_url = channel_url

    def __build_youtube_service(self):
        """
        Builds the YouTube service.
        This method uses the Google API client library to build a service object for interacting
        with the YouTube API.

        Returns:
        (googleapiclient.discovery.Resource): The service object for the YouTube API.

        """
        return build('youtube', 'v3', developerKey=self.__api_key)

    def __get_snippet_using_channel_username(self, youtube, channel_username):
        """
        Gets the snippet data for a YouTube channel using the channel username.

        Args:
        youtube (googleapiclient.discovery.Resource): The service object YouTube object.
        channel_username (str): The channel username of the YouTube channel.

        Returns:
        (dict): The snippet data of the YouTube channel.

        """
        return youtube.search().list(
            q=channel_username,
            part="snippet",
            type="channel",
            maxResults=1
        )

    def __get_snippet_using_id(self, youtube, channel_id):
        """
        Gets the snippet data for a YouTube channel using the channel ID. Can return more full data.

        Args:
        youtube (googleapiclient.discovery.Resource): The service object YouTube object.
        channel_id (str): The ID of the YouTube channel.

        Returns:
        (dict): The snippet data for the YouTube channel.

        """
        return youtube.channels().list(
            part="snippet",
            id=channel_id
        )

    def __get_channel_username_from_url(self, channel_url: str) -> str:
        """
        Gets the channel username from the channel URL and return it.

        Parameters:
        channel_url (str): The URL of the YouTube channel.

        """
        parsed_url = urlparse(channel_url)
        if parsed_url.path.startswith("/@"):
            # Example: "https://www.youtube.com/@Google"
            self.channel_username = unquote(parsed_url.path[2:])
            return True
        elif parsed_url.path.startswith("/channel/"):
            # Example: "https://www.youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ"
            self.channel_username = unquote(parsed_url.path[9:])
            return True
        elif parsed_url.path.startswith("/c/"):
            # Example: "https://www.youtube.com/c/YouTubeCreators"
            self.channel_username = unquote(parsed_url.path[3:])
            return True
        return False

    def get_channel_data(self) -> dict:
        """
        Get the channel data from the channel url.

        It sets the channel_id, channel_title, and channel_description attributes of the YoutubeApi
        object based on the retrieved data.

        """
        if self.__get_channel_username_from_url(self.channel_url):
            if not self.channel_username:
                return False
            youtube = self.__build_youtube_service()
            request = self.__get_snippet_using_channel_username(youtube, self.channel_username)
            response = request.execute()
            response_items = response.get('items', [])
            if response_items:
                self.channel_id = response_items[0]['id']['channelId']
                self.channel_title = response_items[0]['snippet']['title']

                request = self.__get_snippet_using_id(youtube, self.channel_id)
                response = request.execute()
                response_items = response.get('items', [])
                if response_items:
                    self.channel_description = response_items[0]['snippet']['description']
            return True
        return False
