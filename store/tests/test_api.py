import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status, permissions
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(name='Admin book', price='9999.99', author_name='Admin1')
        self.book_2 = Book.objects.create(name='Admin book 2', price=1, author_name='Admin22')
        self.book_3 = Book.objects.create(name='Admin1 book 2', price=1, author_name='NeAdmin333')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Admin1'})
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list', permissions.AllowAny, )
        data = {
            'name': 'adminbook1',
            'price': 150,
            'author_name': 'admin1',
            'description': 'adminadminadmin',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json', )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            'name': 'adminbook1',
            'price': 150,
            'author_name': 'admin1',
            'description': 'adminadminadmin',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, json_data, 'json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
