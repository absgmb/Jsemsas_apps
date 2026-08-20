import json
import os
from decimal import Decimal

from celery import shared_task
from django.conf import settings

from .models import NHIATariff


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def sync_nhia_tariffs(self):
    if not settings.GOOGLE_SHEETS_ID or not settings.GOOGLE_SERVICE_ACCOUNT_JSON:
        return {"status": "skipped", "reason": "Google Sheets configuration missing"}

    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    service_account_value = settings.GOOGLE_SERVICE_ACCOUNT_JSON.strip()
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    # Accept either a filesystem path or the JSON content stored securely in an
    # environment variable. The latter is suitable for PandaStack secrets.
    if os.path.isfile(service_account_value):
        creds = service_account.Credentials.from_service_account_file(
            service_account_value, scopes=scopes
        )
    else:
        creds = service_account.Credentials.from_service_account_info(
            json.loads(service_account_value), scopes=scopes
        )

    service = build("sheets", "v4", credentials=creds, cache_discovery=False)
    values = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=settings.GOOGLE_SHEETS_ID,
            range=settings.GOOGLE_SHEETS_RANGE,
        )
        .execute()
        .get("values", [])
    )

    updated = 0
    for row in values[1:]:
        if len(row) < 4:
            continue
        code, desc, price, category = row[:4]
        active = (
            str(row[4]).strip().lower() not in ("false", "0", "no")
            if len(row) > 4
            else True
        )
        NHIATariff.objects.update_or_create(
            nhis_code=code.strip(),
            defaults={
                "item_description": desc.strip(),
                "unit_price": Decimal(str(price).replace(",", "")),
                "category": category.strip().upper(),
                "is_active": active,
            },
        )
        updated += 1

    return {"status": "ok", "updated": updated}
