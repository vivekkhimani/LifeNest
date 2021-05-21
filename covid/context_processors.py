"""
context_processor for auth persistence in the UI tree.
"""


def user_auth_context(request):
    context = dict()
    if request.user.is_authenticated and request.user.is_active:
        context['logged_in'] = True
        context['current_user'] = request.user
    else:
        context['logged_in'] = False
        context['current_user'] = request.user
    return context
