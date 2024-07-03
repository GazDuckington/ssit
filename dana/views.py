from django.views import View
from django.shortcuts import render

# Create your views here.
class HelloView(View):
    def get(self, request):
        context = {
            "message": "hello",
            "user": request.user
        }
        return render(request, 'hello.html', context)

