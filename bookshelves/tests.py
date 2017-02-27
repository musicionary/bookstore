from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from bookshelves.views import home_page
from bookshelves.models import Bookshelf, Book


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_display_all_bookshelves(self):
        Bookshelf.objects.create(name="Want To Read")
        Bookshelf.objects.create(name="Need To Read")
        response= self.client.get('/')
        self.assertIn('Want To Read', response.content.decode())
        self.assertIn('Need To Read', response.content.decode())



class BookshelfModelTest(TestCase):

    def test_saving_and_retrieving_shelves(self):
        first_shelf = Bookshelf()
        first_shelf.name = "Want To Read"
        first_shelf.save()

        second_shelf = Bookshelf()
        second_shelf.name = "Finished Books"
        second_shelf.save()

        saved_shelves = Bookshelf.objects.all()
        self.assertEqual(saved_shelves.count(), 2)

        first_saved_shelf = saved_shelves[0]
        second_saved_shelf = saved_shelves[1]
        self.assertEqual(first_saved_shelf.name, 'Want To Read')
        self.assertEqual(second_saved_shelf.name, "Finished Books")

class BookModelTest(TestCase):

    def test_saving_and_retrieving_books(self):
        shelf = Bookshelf()
        shelf.name = "Test Shelf"
        shelf.save()

        first_book = Book()
        first_book.name = "Big book"
        first_book.bookshelf_id = shelf.id
        first_book.save()

        second_book = Book()
        second_book.name = "Small book"
        second_book.bookshelf_id = shelf.id
        second_book.save()

        saved_books = Book.objects.all()
        self.assertEqual(saved_books.count(), 2)

        first_saved_book = saved_books[0]
        second_saved_book = saved_books[1]
        self.assertEqual(first_book.bookshelf_id, shelf.id)
        self.assertEqual(first_saved_book.name, 'Big book')
        self.assertEqual(second_saved_book.name, "Small book")


class BookshelfViewTest(TestCase):

    def test_displays_shelf_and_books(self):
        bookshelf = Bookshelf.objects.create(name="Want To Read")
        Book.objects.create(name="Test book", bookshelf=bookshelf)
        Book.objects.create(name="Another book", bookshelf=bookshelf)

        response = self.client.get('/bookshelves/%d/' % (bookshelf.id))
        self.assertTemplateUsed(response, 'bookshelf.html')

        self.assertContains(response, 'Want To Read')

    def test_displays_only_books_for_that_shelf(self):
        correct_shelf = Bookshelf.objects.create()
        Book.objects.create(name='itemey 1', bookshelf=correct_shelf)
        Book.objects.create(name='itemey 2', bookshelf=correct_shelf)
        other_shelf = Bookshelf.objects.create()
        Book.objects.create(name='other shelf item 1', bookshelf=other_shelf)
        Book.objects.create(name='other shelf item 2', bookshelf=other_shelf)

        response = self.client.get('/bookshelves/%d/' % (correct_shelf.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

class NewBookshelfTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/bookshelves/new', data={
                'bookshelf_text': "A new bookshelf"
            }
        )
        self.assertEqual(Bookshelf.objects.count(), 1)
        new_item = Bookshelf.objects.first()
        self.assertEqual(new_item.name, 'A new bookshelf')

    def test_redirect_after_POST(self):
        response = self.client.post('/bookshelves/new', data={
                'bookshelf_text': "A new bookshelf"
            }
        )
        new_shelf = Bookshelf.objects.last()
        self.assertRedirects(response, '/bookshelves/%d/' % (new_shelf.id))

    def test_can_save_a_POST_request_to_an_existing_bookshelf(self):
        other_shelf = Bookshelf.objects.create()
        correct_shelf = Bookshelf.objects.create()

        self.client.post(
            '/bookshelves/%d/new_book' % (correct_shelf.id,),
            data={'book_text': 'A new book for an existing shelf', "bookshelf": '%d' % (correct_shelf.id)}
        )

        self.assertEqual(Book.objects.count(), 1)
        new_book = Book.objects.first()
        self.assertEqual(new_book.name, 'A new book for an existing shelf')
        self.assertEqual(new_book.bookshelf, correct_shelf)

    def test_redirects_to_bookshelf_view(self):
        other_shelf = Bookshelf.objects.create()
        correct_shelf = Bookshelf.objects.create()

        response = self.client.post(
            '/bookshelves/%d/new_book' % (correct_shelf.id,),
            data={'book_text': 'A new book for an existing shelf'}
        )

        self.assertRedirects(response, '/bookshelves/%d/' % (correct_shelf.id))

    def test_passes_correct_list_to_template(self):
        other_shelf = Bookshelf.objects.create()
        correct_shelf = Bookshelf.objects.create()
        response = self.client.get('/bookshelves/%d/' % (correct_shelf.id,))
        self.assertEqual(response.context['bookshelf'], correct_shelf)
