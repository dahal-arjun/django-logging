import json


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with open("log.txt", "a") as f:
            body_str = request.body.decode("utf-8")  # Decode bytes to string
            f.write(json.dumps({
                "endpoint": request.path,
                "method": request.method,
                "body": body_str,  # Use the decoded body string
                "headers": dict(request.headers),
                "query_params": dict(request.GET),
                "user": request.user.username if hasattr(request, 'user') and request.user.is_authenticated else None

            }) + "\n")  # Add newline for readability
        return self.get_response(request)
