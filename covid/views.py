from django.contrib import messages
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .models import Supplier, Requester, Service
from .forms import UserForm, SupplierForm, RequesterForm


# Create your views here.
def index(request):
    try:
        context = {
            'page_name': 'Helping Hand | Home',
        }
        return render(request, 'covid/base.html', context=context)
    except Exception as ex:
        print(ex)  # fixme: add logger support later
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


@transaction.atomic
def supplier_signup(request):
    if request.method == 'POST':
        creation_form = UserCreationForm(request.POST)
        user_form = UserForm(request.POST)
        supplier_form = SupplierForm(request.POST)

        if creation_form.is_valid() and user_form.is_valid() and supplier_form.is_valid():
            creation_form.save()
            username = creation_form.cleaned_data.get('username')
            raw_password = creation_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user_form.save()
            supplier_form.save()
            messages.success(request, 'Your supplier account was created successfully.')
            return redirect('supplier_list')
        else:
            messages.error(request, 'There was an error creating the profile because:')
    else:
        creation_form = UserCreationForm(request.POST)
        user_form = UserForm(request.POST)
        supplier_form = SupplierForm(request.POST)
    return render(request, 'covid/signup.html', {'type': 'Supplier', 'creation': creation_form, 'user': user_form, 'supplier': supplier_form})


@transaction.atomic
def requester_signup(request):
    if request.method == 'POST':
        creation_form = UserCreationForm(request.POST)
        user_form = UserForm(request.POST)
        requester_form = RequesterForm(request.POST)

        if creation_form.is_valid() and user_form.is_valid() and requester_form.is_valid():
            creation_form.save()
            username = creation_form.cleaned_data.get('username')
            raw_password = creation_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user_form.save()
            requester_form.save()
            messages.success(request, 'Your supplier account was created successfully.')
            return redirect('supplier_list')
        else:
            messages.error(request, 'There was an error creating the profile because:')
    else:
        creation_form = UserCreationForm(request.POST)
        user_form = UserForm(request.POST)
        requester_form = SupplierForm(request.POST)
    return render(request, 'covid/signup.html', {'type': 'Requester', 'creation': creation_form, 'user': user_form, 'supplier': requester_form})


def volunteer_signup(request):
    return


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
