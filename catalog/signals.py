from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book
from django.core.cache import cache


@receiver(post_save, sender=Book)
@receiver(post_delete, sender=Book)
def clear_book_cache(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance is not None:
        cache_key = f"book_{instance.pk}"
        cache.delete(cache_key)







