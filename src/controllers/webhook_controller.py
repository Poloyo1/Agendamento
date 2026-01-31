from flask import request, jsonify
from src.services.whatsapp import send_message
from src.services.google_calendar import create_event, is_available
from src.models.session import get_session, update_session, clear_session
from src.models.client import get_client_by_phone

def webhook_handler():
    data = request.json

    phone = data["phone"]
    text = data["text"]["message"].strip()

    client = get_client_by_phone(phone)

    if not client or not client["active"]:
        send_message(phone, "❌ Número não autorizado.")
        return jsonify({"status": "blocked"})

    session = get_session(phone)
    step = session["step"]

    # STEP 1
    if step == 1:
        send_message(
            phone,
            f"Olá! Sou o assistente da {client['name']} 😊\n"
            "Qual serviço deseja agendar?"
        )
        update_session(phone, {"step": 2})

    # STEP 2
    elif step == 2:
        update_session(phone, {
            "service": text,
            "step": 3
        })
        send_message(phone, "📅 Qual a data? (DD/MM/AAAA)")

    # STEP 3
    elif step == 3:
        update_session(phone, {
            "date": text,
            "step": 4
        })
        send_message(phone, "⏰ Qual horário? (HH:MM)")

    # STEP 4
    elif step == 4:
        calendar_id = client["calendar_id"]

        if not is_available(calendar_id, session["date"], text):
            send_message(
                phone,
                "❌ Esse horário já está ocupado.\n"
                "Por favor, escolha outro."
            )
            return jsonify({"status": "busy"})

        event = create_event(
            calendar_id=calendar_id,
            service_name=session["service"],
            date_str=session["date"],
            time_str=text
        )

        send_message(
            phone,
            f"✅ Agendamento confirmado!\n\n"
            f"Serviço: {session['service']}\n"
            f"Data: {session['date']}\n"
            f"Horário: {text}\n\n"
            f"📎 {event['htmlLink']}"
        )

        clear_session(phone)

    return jsonify({"status": "ok"})
