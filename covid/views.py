from django.contrib import messages
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied

from .models import Participant, Service, VerifiedPhone
from .forms import ParticipantForm, MyUserCreationForm, AuthenticationForm


# Create your views here.
def index(request):
    context = {
        'page_name': 'Life Nest | Home',
    }
    return render(request, 'covid/base.html', context=context)


def landing_view(request):
    if request.user.is_authenticated and request.user.is_active:
        context = {
            'page_name': 'Life Nest | Welcome',
        }
        return render(request, 'covid/landing.html', context=context)
    else:
        raise PermissionDenied


@transaction.atomic
def participant_signup(request):
    if request.method == 'POST':
        creation_form = MyUserCreationForm(request.POST)
        participant_form = ParticipantForm(request.POST)

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
        creation_form = MyUserCreationForm(request.POST)
        participant_form = ParticipantForm(request.POST)
    return render(request, 'covid/signup.html',
                  {'page_name': 'Life Nest | Sign Up', 'creation': creation_form, 'participant': participant_form})


@transaction.atomic
def signin(request):
    if request.method == 'POST':
        authentication_form = AuthenticationForm(request.POST)

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
        authentication_form = AuthenticationForm(request.POST)

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
    context = {
        'page_name': 'Helping Hand | Delete'
    }
    # fixme: make users inactive. don't actually delete them. (or we can provide both the options).
    return render(request, 'covid/delete_data.html', context=context)
