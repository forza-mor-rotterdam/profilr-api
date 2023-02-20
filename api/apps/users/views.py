from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


@user_passes_test(lambda u: u.is_superuser)
def config(request):
    return render(
        request,
        "config.html",
        {
            "config": {
                "MSB_API_URL": settings.MSB_API_URL,
                "INCIDENT_API_URL": settings.INCIDENT_API_URL,
                "INCIDENT_API_HEALTH_CHECK_URL": settings.INCIDENT_API_HEALTH_CHECK_URL,
            }
        },
    )
