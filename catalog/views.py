from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic


# Create your views here.
class IndexView(generic.View):
    template_name = "index.html"

    def get(self, request):
        num_books = Book.objects.all().count()
        num_instances = BookInstance.objects.all().count()
        num_instances_available = BookInstance.objects.filter(status__exact="a").count()
        num_authors = Author.objects.count()

        num_visits =  request.session.get("num_visits", 0) + 1
        request.session["num_visits"] = num_visits

        context = {
            "num_books": num_books,
            "num_instances": num_instances,
            "num_instances_available": num_instances_available,
            "num_authors": num_authors,
            "num_visits": num_visits,
        }

        return render(request, self.template_name, context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "book_list.html"
    paginate_by = 2

    # def get_queryset(self):
    #     return Book.objects.all()[:5]

    def get_context_date(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context["some_additional_data"] = "This is some additional data!"
        return context


class BookDetailView(generic.DetailView):
    template_name = "book_detail.html"
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = "author_list"
    template_name = "author_list.html"
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    template_name = "author_detail.html"
    model = Author



