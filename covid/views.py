from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout

from .models import Participant, Service, VerifiedPhone
from .forms import ParticipantForm, MyUserCreationForm, AuthenticationForm, ServiceForm


# Create your views here.
def index(request):
    participants = Participant.objects.all()
    total_services = Service.objects.all().count()
    total_participants = participants.count()
    total_helped = participants.aggregate(Sum('num_helps'))['num_helps__sum']
    context = {
        'page_name': 'Life Nest | Home',
        'total_services': total_services,
        'total_participants': total_participants,
        'total_helped': total_helped,
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
        service_instance = Service.objects.prefetch_related('scam_votes', 'help_votes').get(id=pk)
        is_owner = False
        if service_instance.provider.user == request.user:
            is_owner = True

        has_voted_scam, has_voted_help = False, False
        if service_instance.scam_votes.filter(scam_votes_participants__scam_votes__user=request.user).exists():
            has_voted_scam = True
        if service_instance.help_votes.filter(help_votes_participants__help_votes__user=request.user).exists():
            has_voted_help = True

        return render(request, 'covid/view_service.html',
                      {'page_name': 'Life Nest | View Resource', 'instance': service_instance,
                       'is_owner': is_owner, 'has_voted_scam': has_voted_scam, 'has_voted_help': has_voted_help})
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
            return redirect(reverse('view_service', args=[pk]))
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


def scam_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        curr_participant = Participant.objects.get(user=request.user)
        service_instance = get_object_or_404(Service, pk=pk)
        service_instance.scam_votes.add(curr_participant)
        service_instance.save()
        provider_instance = service_instance.provider
        provider_instance.num_scams += 1
        provider_instance.save()
        return redirect(reverse('view_service', args=[pk]))
    else:
        return redirect('index')


def help_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        curr_participant = Participant.objects.get(user=request.user)
        service_instance = get_object_or_404(Service, pk=pk)
        service_instance.help_votes.add(curr_participant)
        service_instance.save()
        provider_instance = service_instance.provider
        provider_instance.num_helps += 1
        provider_instance.save()
        return redirect(reverse('view_service', args=[pk]))
    else:
        return redirect('index')


def undo_scam_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        curr_participant = Participant.objects.get(user=request.user)
        service_instance = get_object_or_404(Service, pk=pk)
        service_instance.scam_votes.remove(curr_participant)
        service_instance.save()
        provider_instance = service_instance.provider
        provider_instance.num_scams -= 1
        provider_instance.save()
        return redirect(reverse('view_service', args=[pk]))
    else:
        return redirect('index')


def undo_help_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        curr_participant = Participant.objects.get(user=request.user)
        service_instance = get_object_or_404(Service, pk=pk)
        service_instance.help_votes.remove(curr_participant)
        service_instance.save()
        provider_instance = service_instance.provider
        provider_instance.num_helps -= 1
        provider_instance.save()
        return redirect(reverse('view_service', args=[pk]))
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
