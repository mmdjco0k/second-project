from django.http import HttpResponse
from constance import config
from django.urls import reverse


class SiteUpdatingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_updating = config.IS_UPDATING

        if  is_updating:
            if request.path.startswith(reverse('admin:index')):
                return self.get_response(request)

            return HttpResponse("The site is currently updating. Please try again later.")

        return self.get_response(request)