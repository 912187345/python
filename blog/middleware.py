import json
from django.utils import deprecation

class BodyParse(deprecation.MiddlewareMixin):
    def process_request(self,request):
        if request.method == 'POST':
            try:
                request.jsonBody = json.loads(request.body)
            except:
                request.jsonBody = {}
        return

class Token(deprecation.MiddlewareMixin):
    def process_request(self, request):
        return None