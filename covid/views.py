from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout

from .models import Participant, Service, VerifiedPhone
from .forms import ParticipantForm, MyUserCreationForm, AuthenticationForm, ServiceForm


# Create your views here.
def index(request):
    context = {
        'page_name': 'Life Nest | Home',
    }
    if request.user.is_authenticated and request.user.is_active:
        return redirect('landing')
    else:
        return render(request, 'covid/base.html', context=context)


def landing_view(request):
    if request.user.is_authenticated and request.user.is_active:
        services = Service.objects.all()
        context = {
            'page_name': 'Life Nest | Welcome',
            'services': services
        }
        return render(request, 'covid/landing.html', context=context)
    else:
        return redirect('index')


@transaction.atomic
def add_resource(request):
    if request.user.is_authenticated and request.user.is_active:
        if request.method == 'POST':
            service_form = ServiceForm(request.POST or None)
            service_form.fields['price'].label = "Free/Paid?"

            if service_form.is_valid():
                service_instance = service_form.save(commit=False)
                current_user = Participant.objects.get(user=request.user)
                service_instance.provider = current_user
                service_instance.save()
                messages.success(request, "The service was successfully added.")
                return redirect('landing')
            else:
                messages.error(request, 'There was an error creating the service.')

        else:
            service_form = ServiceForm(request.POST or None)
            service_form.fields['price'].label = "Free/Paid?"
        return render(request, 'covid/add_service.html',
                      {'page_name': 'Life Nest | Add Resource', 'service': service_form})
    else:
        return redirect('index')


def view_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        service_instance = Service.objects.get(id=pk)
        is_owner = False
        if service_instance.provider.user == request.user:
            is_owner = True
        return render(request, 'covid/view_service.html',
                      {'page_name': 'Life Nest | View Resource', 'instance': service_instance, 'is_owner': is_owner})
    else:
        return redirect('index')


@transaction.atomic()
def edit_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        service_instance = get_object_or_404(Service, pk=pk)
        if service_instance.provider.user != request.user:
            return HttpResponseForbidden()
        service_form = ServiceForm(request.POST or None, instance=service_instance)
        if request.POST and service_form.is_valid():
            service_form.save()
            return redirect('index')
        else:
            return render(request, 'covid/add_service.html',
                          {'page_name': 'Life Nest | Edit Resource', 'service': service_form})
    else:
        return redirect('index')


def delete_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        service_instance = get_object_or_404(Service, pk=pk)
        if service_instance.provider.user != request.user:
            return HttpResponseForbidden()
        Service.objects.filter(id=pk).delete()
        return redirect('index')
    else:
        return redirect('index')


@transaction.atomic
def participant_signup(request):
    if request.method == 'POST':
        creation_form = MyUserCreationForm(request.POST or None)
        participant_form = ParticipantForm(request.POST or None)

        if creation_form.is_valid() and participant_form.is_valid():
            user_instance = creation_form.save()
            login(request, user_instance)
            participant = participant_form.save(commit=False)
            participant.user = user_instance
            participant.save()
            messages.success(request, 'Your account was created successfully.')
            return redirect('landing')
        else:
            messages.error(request, 'There was an error creating the profile because:')
    else:
        creation_form = MyUserCreationForm(request.POST or None)
        participant_form = ParticipantForm(request.POST or None)
    return render(request, 'covid/signup.html',
                  {'page_name': 'Life Nest | Sign Up', 'creation': creation_form, 'participant': participant_form})


@transaction.atomic
def signin(request):
    if request.method == 'POST':
        authentication_form = AuthenticationForm(request.POST or None)

        if authentication_form.is_valid():
            username = authentication_form.cleaned_data.get('username')
            password = authentication_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if not user:
                authentication_form.add_error(field='password', error='Incorrect password for the username.')
            else:
                login(request, user)
                return redirect('landing')
    else:
        authentication_form = AuthenticationForm(request.POST or None)

    return render(request, 'covid/login.html',
                  {'page_name': 'Life Nest | Sign In', 'authentication': authentication_form})


def reset_password(request):
    return


def add_superuser(request):
    return


def change_information(request):
    return


def signout(request):
    logout(request)
    return redirect('index')


def delete_data(request):
    return
