from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
from django.utils.safestring import SafeString

from .models import Participant, Service, VerifiedPhone, Spammer
from .forms import ParticipantForm, MyUserCreationForm, AuthenticationForm, ServiceForm, UpdateParticipantForm, \
    UpdateUserForm, SpammerForm


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


@sensitive_variables('user_instance')
@sensitive_post_parameters()
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
    return render(request, 'auth/signup.html',
                  {'page_name': 'Life Nest | Sign Up', 'creation': creation_form, 'participant': participant_form})


@transaction.atomic
@sensitive_post_parameters()
@sensitive_variables('username', 'password', 'user')
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

    return render(request, 'auth/login.html',
                  {'page_name': 'Life Nest | Sign In', 'authentication': authentication_form})


@transaction.atomic
@sensitive_post_parameters()
def update_profile(request):
    if request.user.is_authenticated and request.user.is_active:
        participant_instance = get_object_or_404(Participant, user=request.user)
        user_update_form = UpdateUserForm(request.POST or None, instance=request.user)
        participant_update_form = UpdateParticipantForm(request.POST or None, instance=participant_instance)
        if request.POST and participant_update_form.is_valid() and user_update_form.is_valid():
            user_instance = user_update_form.save()
            participant_instance = participant_update_form.save(commit=False)
            participant_instance.user = user_instance
            participant_instance.save()
            return redirect('view_profile')
        else:
            return render(request, 'covid/edit_profile.html',
                          {'page_name': 'Life Nest | Edit Profile', 'participant': participant_update_form,
                           'creation': user_update_form})
    else:
        return redirect('index')


# private method
def manual_field_distinct_patch(distinct_phones):
    all_spammers = Spammer.objects.all()
    final_spammers = list()
    distinct = set(distinct_phones)

    for spammer in all_spammers:
        if spammer.phone in distinct:
            final_spammers.append(spammer)
            distinct.remove(spammer.phone)
        if len(distinct) == 0:
            break
    return final_spammers


# private method
def generate_count_dict(annotation):
    return_dict = dict()
    for it in annotation:
        return_dict[str(it['phone'])] = it['count']
    return return_dict


def report_spam_landing(request):
    if request.user.is_authenticated and request.user.is_active:
        unique_phones_list = Spammer.objects.values_list('phone', flat=True).distinct()
        unique_spammers_list = manual_field_distinct_patch(unique_phones_list)
        phone_count = generate_count_dict(Spammer.objects.values('phone').order_by('-date_reported').annotate(count=Count('phone')))
        return render(request, 'covid/report_spam_landing.html',
                      {'page_name': 'Life Nest | Report Spam', 'spam': unique_spammers_list, 'count': SafeString(phone_count)})
    else:
        return redirect('index')


def expand_spam(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        reporter_instance = Participant.objects.get(user=request.user)
        spammer_instance = get_object_or_404(Spammer, pk=pk)
        phone_instance = spammer_instance.phone
        spammer_info = None
        in_records = Participant.objects.filter(phone=phone_instance).exists()
        if in_records:
            spammer_info = Participant.objects.get(phone=phone_instance)

        already_reported = Spammer.objects.filter(reporter=reporter_instance, phone=phone_instance).exists()
        all_reports = Spammer.objects.filter(phone=phone_instance).all()
        return render(request, 'covid/view_spam.html', {'page_name': 'Life Nest | View Spam', 'reports': all_reports, 'in_records': in_records, 'spammer': spammer_info, 'already_reported': already_reported, 'spam_id': pk})
    else:
        return redirect('index')


@transaction.atomic
@sensitive_post_parameters()
def add_new_spam(request):
    if request.user.is_authenticated and request.user.is_active:
        spam_reporter = Participant.objects.get(user=request.user)
        if request.method == 'POST':
            spammer_form = SpammerForm(request.POST or None, reporter=spam_reporter)
            if spammer_form.is_valid():
                # spammer instance created
                spammer_instance = spammer_form.save(commit=False)
                spammer_instance.reporter = spam_reporter
                spammer_instance.save()
                # spam votes given increase
                giver_instance = Participant.objects.get(user=request.user)
                giver_instance.spam_reports_given += 1
                giver_instance.save()
                # spam votes received increase
                receiver_promise = Participant.objects.filter(phone=spammer_form.cleaned_data.get('phone')).exists()
                if receiver_promise:
                    receiver_instance = Participant.objects.get(phone=spammer_form.cleaned_data.get('phone'))
                    receiver_instance.spam_reports_received += 1
                    receiver_instance.save()
                return redirect(reverse('view_spam', args=[spammer_instance.id]))
            else:
                messages.error(request, "There was an error creating a spammer.")

        else:
            spammer_form = SpammerForm(request.POST or None, reporter=spam_reporter)

        return render(request, 'covid/add_spam.html',
                      {'page_name': 'Life Nest | Add Spam', 'spam': spammer_form})
    else:
        return redirect('index')


def undo_spam_upvote(request, pk=None):
    if request.user.is_authenticated and request.user.is_active:
        curr_spammer_instance = get_object_or_404(Spammer, pk=pk)
        phone = curr_spammer_instance.phone
        reporter_instance = Participant.objects.get(user=request.user)
        unique_spammer_instance = Spammer.objects.get(reporter=reporter_instance, phone=phone)
        unique_spammer_instance.delete()

        # spam votes given decrease
        reporter_instance.spam_reports_given -= 1
        reporter_instance.save()

        # spam votes received decrease
        if Participant.objects.filter(phone=phone).exists():
            receiver_instance = Participant.objects.get(phone=phone)
            receiver_instance.spam_reports_received -= 1
            receiver_instance.save()
        return redirect('spam_view_landing')
    else:
        return redirect('index')


def update_password(request):
    # fixme: need to implement
    return redirect('index')


def signout(request):
    logout(request)
    return redirect('index')


def delete_data(request):
    if request.user.is_authenticated and request.user.is_active:
        Participant.objects.get(user=request.user).delete()
        logout(request)
    return redirect('index')
