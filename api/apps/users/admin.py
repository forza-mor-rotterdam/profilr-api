from apps.users.models import Profile
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name = _("Profile")
#     verbose_name_plural = _("Profile")
#     fk_name = "user"


class ProjectUserAdmin(UserAdmin):
    pass
    # inlines = (ProfileInline,)


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, ProjectUserAdmin)
admin.site.register(Profile, ProfileAdmin)
