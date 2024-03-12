import os
import unittest

from youtube_api.add_youtuber import YoutubeApi


class TestYoutubeApi(unittest.TestCase):
    """A class to test the YoutubeApi class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_extracting_data_from_url_type_1(self):
        """The first type of URL is in the format: "https://www.youtube.com/channel/{channel_id}"""
        api = YoutubeApi("https://www.youtube.com/channel/UCVp3HrjsHf13z4wdV6jDMyw")
        api.get_channel_data()
        self.assertEqual(api.channel_id, 'UCVp3HrjsHf13z4wdV6jDMyw')
        self.assertEqual(api.channel_title, 'Burger Channel')
        self.assertIsNotNone(api.channel_description)

    def test_extracting_data_from_url_type_2(self):
        """The second type of URL is in the format: "https://www.youtube.com/@{username}"""
        api = YoutubeApi("https://www.youtube.com/@teoriaihor")
        api.get_channel_data()
        self.assertEqual(api.channel_id, 'UCUZ1OQmxTIE0uEHplDe7ptg')
        self.assertEqual(api.channel_title, 'Теорія Ігор')
        self.assertIsNotNone(api.channel_description)

    def test_extracting_data_from_url_type_3(self):
        """The third type of URL is in the format: "https://www.youtube.com/c/@{username}"""
        api = YoutubeApi("https://www.youtube.com/c/@burgerchannel")
        api.get_channel_data()
        self.assertEqual(api.channel_id, 'UCVp3HrjsHf13z4wdV6jDMyw')
        self.assertEqual(api.channel_title, 'Burger Channel')
        self.assertIsNotNone(api.channel_description)


if __name__ == '__main__':
    unittest.main()
