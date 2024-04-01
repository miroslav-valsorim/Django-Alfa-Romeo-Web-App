from django.shortcuts import redirect


def require_name(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.profile.first_name and user.profile.last_name:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user_forum_credentials')

    return wrapper
