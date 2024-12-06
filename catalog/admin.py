from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language


class BookInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "date_of_birth", "date_of_death"]
    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]
    search_fields = ["first_name", "last_name"]
    inlines = [BookInline]
    list_per_page = 10

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "display_genre"]
    search_fields = ["title"]
    inlines = [BookInstanceInline]
    list_per_page = 10

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ["book", "status", "borrower", "due_back", "id"]
    list_filter = ["status", "due_back"]
    list_per_page = 10

    fieldsets = (
        (None, {
            "fields": ("book", "imprint", "id")
        }),
        ("Availability", {
            "fields": ("status", "due_back", "borrower")
        }),
    )


admin.site.register(Genre)
admin.site.register(Language)


