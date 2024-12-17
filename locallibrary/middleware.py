from django.shortcuts import redirect
from django.urls import reverse


class AdminAccessMiddleware:
    """
    Middleware to restrict access to the admin login page
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse("admin:index")):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect("/")

        response = self.get_response(request)
        return response
