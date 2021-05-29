"""
context_processor for auth persistence in the UI tree.
"""
from .models import Participant


def user_auth_context(request):
    context = dict()
    if request.user.is_authenticated and request.user.is_active:
        context['verified_phone'] = False
        if Participant.objects.filter(user=request.user).exists():
            participant_instance = Participant.objects.get(user=request.user)
            if participant_instance.verifiedPhone:
                context['verified_phone'] = True
        context['logged_in'] = True
        context['current_user'] = request.user
        context['full_name'] = request.user.get_full_name()
        context['first_name'] = request.user.first_name
    else:
        context['logged_in'] = False
        context['current_user'] = request.user
    return context
