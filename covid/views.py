from django.contrib import messages
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.http import HttpResponse

from .models import Supplier, Requester, Service, VerifiedPhone
from .forms import SupplierForm, RequesterForm, MyUserCreationForm


# Create your views here.
def index(request):
    context = {
        'page_name': 'Helping Hand | Home',
    }
    if request.user.is_authenticated:
        context['logged_in'] = True
        context['current_user'] = request.user
    else:
        context['logged_in'] = False
        context['current_user'] = request.user
    try:
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
        creation_form = MyUserCreationForm(request.POST)
        supplier_form = SupplierForm(request.POST)

        if creation_form.is_valid() and supplier_form.is_valid():
            username = creation_form.cleaned_data.get('username')
            raw_password = creation_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user_instance = creation_form.save(commit=False)
            group = Group.objects.get(name="Supplier")
            user_instance.groups.add(group)
            user_instance.save()
            supplier = supplier_form.save(commit=False)
            supplier.user = user_instance
            supplier.save()
            messages.success(request, 'Your supplier account was created successfully.')
            return redirect('supplier_list')
        else:
            messages.error(request, 'There was an error creating the profile because:')
    else:
        creation_form = MyUserCreationForm(request.POST)
        supplier_form = SupplierForm(request.POST)
    return render(request, 'covid/signup.html',
                  {'page_name': 'Helping Hand | Supplier', 'type': 'Supplier', 'creation': creation_form, 'supplier': supplier_form})


@transaction.atomic
def requester_signup(request):
    if request.method == 'POST':
        creation_form = MyUserCreationForm(request.POST)
        requester_form = RequesterForm(request.POST)

        if creation_form.is_valid() and requester_form.is_valid():
            username = creation_form.cleaned_data.get('username')
            raw_password = creation_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user_instance = creation_form.save(commit=False)
            group = Group.objects.get(name="Supplier")
            user_instance.groups.add(group)
            user_instance.save()
            requester = requester_form.save(commit=False)
            requester.user = user_instance
            requester.save()
            messages.success(request, 'Your supplier account was created successfully.')
            return redirect('supplier_list')
        else:
            messages.error(request, 'There was an error creating the profile because:')
    else:
        creation_form = MyUserCreationForm(request.POST)
        requester_form = SupplierForm(request.POST)
    return render(request, 'covid/signup.html',
                  {'page_name': 'Helping Hand | Requester', 'type': 'Requester', 'creation': creation_form, 'supplier': requester_form})


def supplier_signin(request):
    return


def requester_signin(request):
    return


def reset_password(request):
    return


def verify_phone_number(request):
    try:
        if request.method == 'POST':
            get_value = request.body
            print(get_value)
            phone_number = request.POST.get("phone_number")
            print(phone_number)
            # noinspection PyBroadException
            try:
                VerifiedPhone.objects.create(phone=phone_number)
                return HttpResponse(status=201)
            except Exception as ex:
                print(ex)  # fixme: enable logging for later
                return redirect('fallback')

        else:
            return redirect('index')

    except Exception as ex:
        print(ex)
        return redirect('404')


def change_information(request):
    return


def signout(request):
    try:
        logout(request)
        return redirect('index')
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
