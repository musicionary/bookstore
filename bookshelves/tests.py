from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from bookshelves.views import home_page
from bookshelves.models import Bookshelf

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/',
            data={'bookshelf_text': "A new bookshelf"}
        )
        self.assertIn("A new bookshelf", response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


class BookshelfModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Bookshelf()
        first_item.name = "Want To Read"
        first_item.save()

        second_item = Bookshelf()
        second_item.name = "Finished Books"
        second_item.save()

        saved_items = Bookshelf.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.name, 'Want To Read')
        self.assertEqual(second_saved_item.name, "Finished Books")
