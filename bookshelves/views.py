from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return render(request, 'home.html', {
        'new_bookshelf_text': request.POST.get('bookshelf_text', ''),
    })
