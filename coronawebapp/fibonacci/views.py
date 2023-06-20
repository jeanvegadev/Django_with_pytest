from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from fibonacci.fibonacci_dinamico import fibonacci_dynamic
# Create your views here.



class FiboView(View):
    def get(self, request, *args, **kwargs):
        n = int(request.GET["n"])
        fibo_n = fibonacci_dynamic(n)
        return JsonResponse({'foo': fibo_n})