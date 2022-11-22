from apps.incidents.models import Incident
from apps.status.tasks import update_status
from deepdiff import DeepDiff
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Incident, dispatch_uid="incident_pre_save")
def incident_pre_save(sender, instance, **kwargs):
    if instance.id is None and instance.msb_data:
        instance.update_fields()

    elif instance.id is not None:
        current = instance
        previous = Incident.objects.get(id=instance.id)
        ddiff = DeepDiff(
            current.msb_data, previous.msb_data, verbose_level=2, view="tree"
        )
        values_changed = ddiff.get("values_changed", [])

        if ddiff:
            for changed in values_changed:
                updated_field = changed.path(output_format="list")[-1]
                priority_fields = ["spoed"]
                status_fields = ["status"]
                if updated_field in priority_fields:
                    instance.spoed = current.msb_data.get(updated_field)
                if updated_field in status_fields:
                    print("status changed")
                    print(instance.user_token)
                    if instance.user_token:
                        update_status.delay(instance.id, instance.user_token)

                print(changed.path(output_format="list")[-1])

            # instance.update_fields()
