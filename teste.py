from src.services.google_calendar import create_event, is_available
from src.database.db import save_appointment



if is_available("primary", "29/01/2026", "15:40"):
    event = create_event(
        "primary",
        "TESTE FINAL",
        "29/01/2026",
        "15:40"
    )
    print(event)
    save_appointment(
    phone="11999999999",
    service="Corte de cabelo",
    date="2026-01-27",
    time="15:40",
    google_event_id=event["id"]
)
else:
    print("❌ Horário indisponível")




print("✅ Evento criado")
print("🔗 Link:", event["htmlLink"])
