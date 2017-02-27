from django.shortcuts import redirect, render
from django.http import HttpResponse
from bookshelves.models import Bookshelf, Book


def home_page(request):
    bookshelves = Bookshelf.objects.all()
    return render(request, 'home.html', {'bookshelves': bookshelves})

def new_bookshelf(request):
    bookshelf = Bookshelf.objects.create(name=request.POST['bookshelf_text'])
    return redirect('/bookshelves/%d/' % (bookshelf.id))

def view_bookshelf(request, bookshelf_id):
    bookshelf = Bookshelf.objects.get(id=bookshelf_id)
    books = Book.objects.filter(bookshelf=bookshelf)
    return render(request, 'bookshelf.html', {'bookshelf': bookshelf, "books":books})

def new_book(request, bookshelf_id):
    bookshelf = Bookshelf.objects.get(id=bookshelf_id)
    book = Book.objects.create(name=request.POST['book_text'], bookshelf=bookshelf)
    return redirect('/bookshelves/%d/' % (bookshelf.id))
