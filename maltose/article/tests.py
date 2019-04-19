import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Article


class ModelTests(TestCase):

    def test_model_to_dict(self):
        """
        测试模型的to_dict方法
        """
        article = Article(
            title="test-title",
            slug="test-slug",
            source='#source',
        )
        article.save()
        self.assertDictEqual(article.to_dict(fields=['title']), {"title": 'test-title'})
        self.assertIsInstance(article.to_dict()['create_time'], str)
        self.assertListEqual(article.to_dict(WTF=[{"1": 'test'}, {'2': 'test'}])['WTF'], [{"1": 'test'}, {'2': 'test'}])
        self.assertDictEqual(article.to_dict(exclude=['id', 'create_time', 'update_time']),
                             {'title': 'test-title', 'slug': 'test-slug', 'source': '#source',
                              'body': '', 'is_draft': True, 'is_public': True, })

    def test_api(self):
        # 创建用户并登陆
        get_user_model().objects.create_superuser('Test', 'Test@qq.com', 'Test')
        self.assertIs(self.client.login(username='Test', password='Test'), True)
