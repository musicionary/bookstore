from django.shortcuts import redirect, render
from django.http import HttpResponse
from bookshelves.models import Bookshelf


def home_page(request):
    if request.method == 'POST':
        Bookshelf.objects.create(name=request.POST['bookshelf_text'])
        return redirect('/')

    bookshelves = Bookshelf.objects.all()
    return render(request, 'home.html', {'bookshelves': bookshelves})
