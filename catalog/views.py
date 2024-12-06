from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
    paginate_by = 2

    # def get_queryset(self):
    #     return Book.objects.all()[:5]

    def get_context_date(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context["some_additional_data"] = "This is some additional data!"
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = "author_list"
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = 10
    template_name = "catalog/bookinstance_list_borrowed_user.html"

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )

class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = 3
    permission_required = "catalog.can_mark_returned"
    template_name = "catalog/bookinstance_list_borrowed.html"
