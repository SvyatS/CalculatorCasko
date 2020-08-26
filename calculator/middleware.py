class ActionsMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        responce = self._get_response(request)
        return responce
