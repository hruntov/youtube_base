from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.paginator import Page, Paginator
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .forms import CommentForm
from .models import Category, Comment, Youtuber
from .views import CommentAddView, YoutuberDetailView, YoutuberList


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


class YoutuberDetailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.youtuber = Youtuber.objects.create(channel_title='Test Youtuber',
                                                channel_description='Test Description')
        self.view = YoutuberDetailView()

    def _create_request(self, method, data=None):
        if method.lower() == 'post':
            request = self.factory.post(reverse('youtuber_detail',
                                                args=[self.youtuber.slug_name]), data or {})
        else:
            request = self.factory.get(reverse('youtuber_detail', args=[self.youtuber.slug_name]))
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request

    def test_add_comment_authenticated(self):
        request = self._create_request('post', {'text': 'Test Comment'})
        request.user = self.user

        view = CommentAddView.as_view()
        response = view(request, slug_name=self.youtuber.slug_name)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, 'Test Comment')

    def test_add_comment_unauthenticated(self):
        request = self._create_request('post', {'text': 'Test Comment'})
        request.user = AnonymousUser()

        view = CommentAddView.as_view()
        response = view(request, slug_name=self.youtuber.slug_name)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

    def test_add_comment_invalid_form(self):
        request = self._create_request('post', {'text': ''})
        request.user = self.user

        view = CommentAddView.as_view()
        response = view(request, slug_name=self.youtuber.slug_name)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)
