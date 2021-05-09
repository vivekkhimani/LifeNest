from django.db.models import QuerySet
from django.shortcuts import render, redirect
from .models import Supplier, Requester, Service


# Create your views here.
def index(request):
    try:
        context = {
            'page_name': 'Helping Hand | Home',
        }
        return render(request, 'covid/base.html', context=context)
    except Exception as ex:
        print(ex)   # fixme: add logger support later
        return redirect('404')


def supplier_list(request):
    try:
        resource_list: QuerySet[Service] = Service.objects.all()
        suppliers: QuerySet[Supplier] = Supplier.objects.all()
        requesters: QuerySet[Requester] = Requester.objects.all()
        print(suppliers[0])
        print(suppliers[0].service_set.all())
        print(requesters[0].service_set.all())
        print(resource_list)
        print(resource_list[5].supplier.all())
        context = {
            'page_name': 'Helping Hand | Home',
            'resource_list': resource_list,
        }
        return render(request, 'covid/suppliers_list.html', context=context)
    except Exception as ex:
        print(ex)  # fixme: add logger support later
        return redirect('404')


def suppliers(request):
    try:
        context = {
            'page_name': 'Helping Hand | Get Started'
        }
        return render(request, 'covid/auth.html', context=context)
    except Exception as ex:
        print(ex)
        return redirect('404')


def logout(request):
    try:
        context = {
            'page_name': 'Helping Hand | Logout'
        }
        return render(request, 'covid/logout.html', context=context)
    except Exception as ex:
        print(ex)
        return redirect('404')


def delete_data(request):
    try:
        context = {
            'page_name': 'Helping Hand | Delete'
        }
        return render(request, 'covid/delete_data.html', context=context)
    except Exception as ex:
        print(ex)
        return redirect('404')


def fallback(request):
    context = {
        'page_name': 'HTTP: 404'
    }
    return render(request, 'covid/404.html', context=context)
