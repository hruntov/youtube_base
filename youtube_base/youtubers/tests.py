from django.core.paginator import Page, Paginator
from django.test import TestCase

from .models import Category, Youtuber
from .views import YoutuberList


class PaginationTest(TestCase):
    def setUp(self):
        self.youtuber_list = YoutuberList()
        for category in range(5):
            category = Category.objects.create(name=f'Category {category}',
                                               description=f'Description {category}')
            for name in range(2):
                youtuber = Youtuber.objects.create(channel_title=f'Youtuber {name}\
                                                        for Category {category}',
                                                   channel_description=f'Description {name}\
                                                        for Category {category}')
                youtuber.categories.add(category)

    def test_pagination(self):
        test_data = Youtuber.objects.all()
        page_data = self.youtuber_list._get_paginated_data(test_data, page=1)
        self.assertIsInstance(page_data, Page)

        page_data = self.youtuber_list._get_paginated_data(test_data, page=9999)
        self.assertIsInstance(page_data, Page)
        self.assertEqual(page_data.number, 4)

        page_data = self.youtuber_list._get_paginated_data(test_data, page='Not the integer!')
        self.assertIsInstance(page_data, Page)
        self.assertEqual(page_data.number, 1)
