class NoCacheForAuthenticatedMiddleware:
    """Prevent browsers from serving stale authenticated pages from the back-forward cache."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            response['Cache-Control'] = 'no-store'
        return response
