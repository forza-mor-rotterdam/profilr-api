from datetime import datetime

import celery
from celery import shared_task

DEFAULT_RETRY_DELAY = 2
MAX_RETRIES = 6


class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception,)
    max_retries = MAX_RETRIES
    default_retry_delay = DEFAULT_RETRY_DELAY


@shared_task(bind=True, base=BaseTaskWithRetry)
def update_status(self, incident_id, user_token):
    print("task update_status START")
    from apps.incidents.models import Incident
    from apps.services.msb import MSBService
    from apps.status.models import Status, StatusChoices

    instance = Incident.objects.get(id=incident_id)
    data = MSBService.get_mutatieregels(instance.external_id, user_token).get("result")

    # print(status)
    # status_str_date = data.get(from_status_to_datefield_name.get(status, {}))
    # if status_str_date is not None:
    #     status_date = datetime.strptime(status_str_date, dt_format)
    # else:
    #     status_date = sorted([datetime.strptime(v, dt_format) for k, v in data.items() if k in date_keys and v is not None])[0]

    # if not Status.objects.filter(created_at=status_date):
    #     status_data = {
    #         "state": MSB_TO_SIGNALS_STATE.get(data.get("status"),  workflow.GEMELD),
    #         "text": "",
    #         "send_email": False,
    #         "_signal": self.signal,
    #     }
    #     status_instance = Status.objects.create(**status_data)
    #     status_instance.created_at = status_date
    #     status_instance.save(update_fields=['created_at'])
    #     self.signal.status = status_instance
    #     self.signal.save(update_fields=['status'])

    statuses_created_at = instance.statuses.all().values_list("created_at", flat=True)

    def get_status(status_details: list):
        status_parts = next(
            iter([t.get("value") for t in status_details if t.get("key") == "Status"]),
            "Nieuw",
        ).split("->")
        status = status_parts[-1].strip()
        print(status)
        status_choice, created = StatusChoices.objects.get_or_create(name=status)
        return status_choice

    not_existing_statusen = [
        Status(
            state=get_status(m.get("details", [])),
            text=m.get("opmerking"),
            send_email=False,
            incident=instance,
            extra_properties=m,
            created_at=datetime.strptime(m.get("datum"), "%Y-%m-%dT%H:%M:%S"),
        )
        for m in data
        if datetime.strptime(m.get("datum"), "%Y-%m-%dT%H:%M:%S")
        not in statuses_created_at
    ]
    Status.objects.bulk_create(not_existing_statusen)
    instance.status = instance.statuses.first()
    instance.save()

    print("task update_status DONE")
