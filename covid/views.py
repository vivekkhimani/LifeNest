from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.cache import cache_page
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
from django.utils.safestring import SafeString
from django.utils import timezone
from django.core.cache import caches

from .firebase_auth import phone_auth_initialize, find_user, delete_user
from .decorators import phone_number_verified
from .models import Participant, Service, Spammer
from .forms import ParticipantForm, MyUserCreationForm, AuthenticationForm, ServiceForm, UpdateParticipantForm, \
    UpdateUserForm, SpammerForm, UpdatePhoneForm

import logging

logger = logging.getLogger(__name__)
phone_auth_initialize()

resource_cache = caches['resource_list']


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
    services = resource_cache.get("resource_list")
    print(services)
    if not services:
        services = Service.objects.all()
        resource_cache.set("resource_list", services)
    context = {
        'page_name': 'Life Nest | Welcome',
        'services': services
    }
    return render(request, 'covid/landing.html', context=context)


@transaction.atomic
@phone_number_verified
@login_required
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
                resource_cache.set("resource_list", None)
                messages.success(request, "The service was successfully added.")
                return redirect('landing')
            else:
                messages.error(request, 'There was an error creating the service.')
                logger.info("service form invalidated.")

        else:
            service_form = ServiceForm(request.POST or None)
            service_form.fields['price'].label = "Free/Paid?"
        return render(request, 'covid/add_service.html',
                      {'page_name': 'Life Nest | Add Resource', 'service': service_form})
    else:
        return redirect('index')


def view_resource(request, pk=None):
    if isinstance(pk, int):
        service_instance = Service.objects.prefetch_related('scam_votes', 'help_votes').get(id=pk)
    else:
        return redirect('index')

    if request.user.is_authenticated and request.user.is_active:
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
        return render(request, 'covid/view_service.html',
                      {'page_name': 'Life Nest | View Resource', 'instance': service_instance})


@transaction.atomic()
@phone_number_verified
@login_required
def edit_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        service_instance = get_object_or_404(Service, pk=pk)
        if service_instance.provider.user != request.user:
            return HttpResponseForbidden()
        service_form = ServiceForm(request.POST or None, instance=service_instance)
        if request.POST and service_form.is_valid():
            service_form.save()
            resource_cache.set("resource_list", None)
            return redirect(reverse('view_service', args=[pk]))
        else:
            return render(request, 'covid/add_service.html',
                          {'page_name': 'Life Nest | Edit Resource', 'service': service_form})
    else:
        return redirect('index')


@phone_number_verified
@login_required
def delete_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        service_instance = get_object_or_404(Service, pk=pk)
        if service_instance.provider.user != request.user:
            return HttpResponseForbidden()
        Service.objects.filter(id=pk).delete()
        resource_cache.set("resource_list", None)
        return redirect('index')
    else:
        return redirect('index')


@login_required
def scam_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        curr_participant = Participant.objects.get(user=request.user)
        service_instance = get_object_or_404(Service, pk=pk)
        service_instance.scam_votes.add(curr_participant)
        service_instance.save()
        resource_cache.set("resource_list", None)
        provider_instance = service_instance.provider
        provider_instance.num_scams += 1
        provider_instance.save()
        return redirect(reverse('view_service', args=[pk]))
    else:
        return redirect('index')


@login_required
def help_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        curr_participant = Participant.objects.get(user=request.user)
        service_instance = get_object_or_404(Service, pk=pk)
        service_instance.help_votes.add(curr_participant)
        service_instance.save()
        resource_cache.set("resource_list", None)
        provider_instance = service_instance.provider
        provider_instance.num_helps += 1
        provider_instance.save()
        return redirect(reverse('view_service', args=[pk]))
    else:
        return redirect('index')


@login_required
def undo_scam_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        curr_participant = Participant.objects.get(user=request.user)
        service_instance = get_object_or_404(Service, pk=pk)
        service_instance.scam_votes.remove(curr_participant)
        service_instance.save()
        resource_cache.set("resource_list", None)
        provider_instance = service_instance.provider
        provider_instance.num_scams -= 1
        provider_instance.save()
        return redirect(reverse('view_service', args=[pk]))
    else:
        return redirect('index')


@login_required
def undo_help_resource(request, pk=None):
    if request.user.is_authenticated and request.user.is_active and isinstance(pk, int):
        curr_participant = Participant.objects.get(user=request.user)
        service_instance = get_object_or_404(Service, pk=pk)
        service_instance.help_votes.remove(curr_participant)
        service_instance.save()
        resource_cache.set("resource_list", None)
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
    if request.user.is_authenticated and request.user.is_active:
        return redirect('index')

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
            logger.info("signup form invalidated.")
    else:
        creation_form = MyUserCreationForm(request.POST or None)
        participant_form = ParticipantForm(request.POST or None)
        print(participant_form.fields)
    return render(request, 'auth/signup.html',
                  {'page_name': 'Life Nest | Sign Up', 'creation': creation_form, 'participant': participant_form})


@transaction.atomic
@sensitive_post_parameters()
@sensitive_variables('username', 'password', 'user')
def signin(request):
    if request.user.is_authenticated and request.user.is_active:
        return redirect('index')

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
@login_required
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
            return redirect('index')
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


@phone_number_verified
@login_required
def report_spam_landing(request):
    if request.user.is_authenticated and request.user.is_active:
        unique_phones_list = Spammer.objects.values_list('phone', flat=True).distinct()
        unique_spammers_list = manual_field_distinct_patch(unique_phones_list)
        phone_count = generate_count_dict(
            Spammer.objects.values('phone').order_by('-date_reported').annotate(count=Count('phone')))
        return render(request, 'covid/report_spam_landing.html',
                      {'page_name': 'Life Nest | Report Spam', 'spam': unique_spammers_list,
                       'count': SafeString(phone_count)})
    else:
        return redirect('index')


@phone_number_verified
@login_required
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
        return render(request, 'covid/view_spam.html',
                      {'page_name': 'Life Nest | View Spam', 'reports': all_reports, 'in_records': in_records,
                       'spammer': spammer_info, 'already_reported': already_reported, 'spam_id': pk})
    else:
        return redirect('index')


@transaction.atomic
@sensitive_post_parameters()
@phone_number_verified
@login_required
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


@phone_number_verified
@login_required
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


@transaction.atomic
@sensitive_post_parameters()
@sensitive_variables()
@login_required
def update_password(request):
    if request.user.is_authenticated and request.user.is_active:
        if request.method == 'POST':
            password_change_form = PasswordChangeForm(request.user, request.POST or None)

            if password_change_form.is_valid():
                participant_instance = Participant.objects.get(user=request.user)
                user = password_change_form.save()
                participant_instance.user = user
                participant_instance.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully changed.')
                return redirect('landing')
            else:
                messages.error(request, 'Error updating your password.')
        else:
            password_change_form = PasswordChangeForm(request.user, request.POST or None)
        return render(request, 'auth/change_password.html',
                      {'page_name': 'Life Nest | Password Change', 'password_change': password_change_form})
    else:
        return redirect('index')


@login_required
def signout(request):
    logout(request)
    return redirect('index')


@login_required
def delete_data(request):
    if request.user.is_authenticated and request.user.is_active:
        User.objects.get(username=request.user.get_username()).delete()
        logout(request)
        logger.warning("An account was deleted by the user himself.")
    return redirect('index')


@login_required
def render_phone_auth_view(request):
    if request.user.is_authenticated and request.user.is_active:
        participant_instance = Participant.objects.get(user=request.user)
        if not participant_instance.verifiedPhone:
            return render(request, 'covid/phone_auth_view.html',
                          {'page_name': 'Life Nest | Phone Verification', 'current_phone': participant_instance.phone})
        else:
            return redirect('index')
    else:
        return redirect('index')


@login_required
def confirm_phone_auth_view(request):
    if request.user.is_authenticated and request.user.is_active:
        participant_instance = Participant.objects.get(user=request.user)
        if not participant_instance.verifiedPhone:
            phone = participant_instance.phone
            if find_user(str(phone)):
                participant_instance.verifiedPhone = True
                participant_instance.save()
            return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')


@transaction.atomic
@login_required
def change_phone_view(request):
    if request.user.is_authenticated and request.user.is_active:
        yesterday = timezone.now() - timezone.timedelta(days=1)
        if Participant.objects.filter(user=request.user, lastPhoneUpdate__gt=yesterday).exists():
            can_access = False
        else:
            can_access = True

        participant_instance = Participant.objects.get(user=request.user)
        if can_access:
            phone = participant_instance.phone
            form = UpdatePhoneForm(request.POST or None, instance=participant_instance,
                                   participant=participant_instance)
            if request.POST and form.is_valid():
                if find_user(str(phone)):
                    delete_user(str(phone))
                new_phone = form.cleaned_data.get('phone')
                participant_instance.phone = new_phone
                participant_instance.verifiedPhone = False
                participant_instance.lastPhoneUpdate = timezone.now()
                participant_instance.save()
                return redirect('render_phone_auth')
            else:
                return render(request, 'covid/update_phone_view.html',
                              {'page_name': 'Life Nest | Update Phone', 'form': form, 'can_access': can_access})
        else:
            last_update = participant_instance.lastPhoneUpdate
            delta = last_update - yesterday
            return render(request, 'covid/update_phone_view.html',
                          {'page_name': 'Life Nest | Update Phone', 'form': None, 'can_access': can_access,
                           'hours_remaining': delta.seconds // 3600})

    else:
        return redirect('index')
