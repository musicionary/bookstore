from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from bookshelves.views import home_page


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'bookshelf_text': "A new bookshelf"})
        self.assertIn("A new bookshelf", response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
