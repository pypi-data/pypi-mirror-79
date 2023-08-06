import logging
from django.http import HttpRequest

logger = logging.getLogger(__name__)


class UserPagesViews(object):
    def __init__(self, get_response):
        logger.debug(f"{__name__} initialization")
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        logger.debug(f"{__name__} call")

        if request.user.is_authenticated and \
                request.method == HttpRequest.GET and \
                hasattr(request.user, "page_views_counter"):
            setattr(request.user,
                    "page_views_counter",
                    getattr(request.user, "page_views_counter") + 1)
            request.user.save()
        response = self.get_response(request)
        return response
