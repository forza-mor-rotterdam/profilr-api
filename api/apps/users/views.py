# from users.models import Profile
from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.shortcuts import render


@user_passes_test(lambda u: u.is_superuser)
def show_profiles(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, username, first_name, email, is_staff FROM public.auth_user"
        )
        users = cursor.fetchall()

    profiles = []
    error = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM public.users_profile")
            profiles = cursor.fetchall()
    except Exception as e:
        error = f"Error: {e}"

    # return row
    return render(
        request,
        "profiles.html",
        {
            "profiles": profiles,
            "error": error,
            "users": users,
        },
    )
