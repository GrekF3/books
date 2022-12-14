from unittest import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(name='Admin book', price='9999.99', author_name='admin', description='adminadmin')
        book_2 = Book.objects.create(name='Admin book 2', price=1, author_name='admin2', description='adminadmin2')
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Admin book',
                'price': '9999.99',
                'author_name': 'admin',
                'description': 'adminadmin',
            },
            {
                'id': book_2.id,
                'name': 'Admin book 2',
                'price': '1.00',
                'author_name': 'admin2',
                'description': 'adminadmin2',
            }
        ]
        self.assertEqual(expected_data, data)
