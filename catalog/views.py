import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from catalog.forms import RenewBookModelForm
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView


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


class RenewBookLibrarianFormView(PermissionRequiredMixin, FormView):
    template_name = "catalog/book_renew_librarian.html"
    form_class = RenewBookModelForm
    success_url = reverse_lazy("all-borrowed")
    permission_required = "catalog.can_mark_returned"

    def form_valid(self, form):
        book_instance = get_object_or_404(BookInstance, pk=self.kwargs["pk"])
        book_instance.due_back = form.cleaned_data["due_back"]
        book_instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["book_instance"] = get_object_or_404(BookInstance, pk=self.kwargs["pk"])
        return context


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]
    initial = {"date_of_birth": "11/11/2023"}
    permission_required = "catalog.add_author"


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = "__all__"
    permission_required = "catalog.change_author"


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy("authors")
    permission_required = "catalog.delete_author"
    template_name_suffix = "_delete"

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )
