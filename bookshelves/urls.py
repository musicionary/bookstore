from django.conf.urls import url
from bookshelves import views

urlpatterns = [
    url(r'^new$', views.new_bookshelf, name='new_bookshelf'),
    url(r'^(\d+)/$', views.view_bookshelf, name='view_bookshelf'),
    url(r'^(\d+)/new_book$', views.new_book, name='new_book'),
]
