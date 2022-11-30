from apps.incidents.models.mixins import CreatedUpdatedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

User = get_user_model()


class Profile(CreatedUpdatedModel):
    """
    The profile model for a user
    """

    user = models.OneToOneField(
        to=User,
        related_name="profile",
        verbose_name=_("profile"),
        on_delete=models.CASCADE,
    )

    filters = models.JSONField(default=dict)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)
