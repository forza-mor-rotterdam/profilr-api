from apps.status.models import Status
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now


@receiver(pre_save, sender=Status, dispatch_uid="status_pre_save")
def status_pre_save(sender, instance, **kwargs):
    if not instance.id:
        print("status_pre_save create")
        if not instance.created_at:
            print("created_at not set")
            instance.created_at = now()


@receiver(post_save, sender=Status, dispatch_uid="status_post_save")
def status_post_save(sender, instance, created, **kwargs):
    if created:
        print(instance.created_at)
