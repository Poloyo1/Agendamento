from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import GOOGLE_CREDENTIALS_FILE
import pytz

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TZ = pytz.timezone("America/Sao_Paulo")

creds = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_FILE,
    scopes=SCOPES
)

calendar_service = build("calendar", "v3", credentials=creds)


def is_available(calendar_id, date_str, time_str, duration=30):
    calendar_id = calendar_id.strip()

    naive_start = datetime.strptime(
        f"{date_str} {time_str}", "%d/%m/%Y %H:%M"
    )
    start = TZ.localize(naive_start)
    end = start + timedelta(minutes=duration)

    events = calendar_service.events().list(
        calendarId=calendar_id,
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True
    ).execute()

    return len(events.get("items", [])) == 0


def create_event(calendar_id, service_name, date_str, time_str, duration=30):
    calendar_id = calendar_id.strip()

    naive_start = datetime.strptime(
        f"{date_str} {time_str}", "%d/%m/%Y %H:%M"
    )
    start = TZ.localize(naive_start)
    end = start + timedelta(minutes=duration)

    event_body = {
        "summary": service_name,
        "start": {
            "dateTime": start.isoformat()
        },
        "end": {
            "dateTime": end.isoformat()
        }
    }

    created_event = calendar_service.events().insert(
        calendarId=calendar_id,
        body=event_body
    ).execute()

    return {
        "id": created_event["id"],
        "htmlLink": created_event["htmlLink"]
    }
