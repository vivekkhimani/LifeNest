from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    context = {
        'page_name': 'Heping Hand | Home',
    }
    return render(request, 'covid/base.html', context=context)
