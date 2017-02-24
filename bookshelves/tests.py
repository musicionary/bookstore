from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from bookshelves.views import home_page
from bookshelves.models import Bookshelf


class HomePageTest(TestCase):

    def test_only_saves_items_when_needed(self):
        self.client.get('/')
        self.assertEqual(Bookshelf.objects.count(), 0)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={
                'bookshelf_text': "A new bookshelf"
            }
        )
        self.assertEqual(Bookshelf.objects.count(), 1)
        new_item = Bookshelf.objects.first()
        self.assertEqual(new_item.name, 'A new bookshelf')

    def test_redirect_after_POST(self):
        response = self.client.post('/', data={
                'bookshelf_text': "A new bookshelf"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_display_all_bookshelves(self):
        Bookshelf.objects.create(name="Want To Read")
        Bookshelf.objects.create(name="Need To Read")
        response= self.client.get('/')
        self.assertIn('Want To Read', response.content.decode())
        self.assertIn('Need To Read', response.content.decode())



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
