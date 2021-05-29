from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from .models import Participant


def phone_number_verified(function):
    def wrap(request, *args, **kwargs):
        participant = Participant.objects.get(user=request.user)
        if participant.verifiedPhone:
            return function(request, *args, **kwargs)
        else:
            return redirect('render_phone_auth')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
