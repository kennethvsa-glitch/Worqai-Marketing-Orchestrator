"""Fast, source-sensitive replies for DMs, comments, and community messages."""

from __future__ import annotations

import re


def build_message_reply(request: str, message: str) -> dict[str, object]:
    cleaned = re.sub(r"\s+", " ", message).strip()
    lowered = cleaned.lower()
    intent = _intent(lowered)
    spanish = _is_spanish(lowered)
    recommended = _reply_for(intent, cleaned, spanish=spanish)
    short = _short_reply_for(intent, spanish=spanish)
    return {
        "format": "message reply",
        "intent": intent,
        "language": "es-LatAm" if spanish else "en",
        "concern_heard": _concern_summary(intent, cleaned, spanish=spanish),
        "recommended_reply": recommended,
        "short_reply": short,
        "friendly_reply": f"{recommended} {'Puede verlo en worqai.io.' if spanish else 'You can see it at worqai.io.'}",
        "tone_rules": [
            "Answer the exact concern before explaining the product.",
            "Avoid guaranteed interviews, rankings, or ATS passage.",
            "State that WorqAI adapts real experience and does not invent it when relevant.",
            "Use one next step and keep the reply proportional to the message.",
        ],
        "follow_up_question": _follow_up_for(intent, spanish=spanish),
        "source_request": request,
        "source_message": message,
    }


def _intent(text: str) -> str:
    if any(word in text for word in ("gratis", "free", "tarjeta", "card", "pago", "pay", "precio", "price")):
        return "pricing_or_free_access"
    if any(word in text for word in ("privacidad", "privacy", "datos", "data", "seguro", "secure")):
        return "privacy_or_data"
    if any(word in text for word in ("ats", "filtro", "filters", "reclutador", "recruiter")):
        return "ats_or_screening"
    if any(word in text for word in ("inventa", "fake", "mentir", "lie", "experiencia", "fabricate")):
        return "trust_no_invention"
    if any(word in text for word in ("cómo", "como", "how", "usar", "funciona", "works")):
        return "how_it_works"
    if any(word in text for word in ("error", "bug", "no funciona", "doesn't work", "not working")):
        return "product_problem"
    return "general_interest"


def _reply_for(intent: str, message: str, *, spanish: bool) -> str:
    if spanish:
        replies = {
            "pricing_or_free_access": "Sí, puede probar el análisis y su primera adaptación gratis, sin tarjeta. Después de registrarse puede empezar con una vacante real.",
            "privacy_or_data": "Es una pregunta importante. El CV contiene información sensible, así que conviene revisar la política de privacidad y compartir solo lo necesario. No voy a prometer un manejo específico que la política publicada no confirme.",
            "ats_or_screening": "Sí, WorqAI compara el CV con los requisitos de la vacante. Eso ayuda a mostrar mejor la relevancia, pero no garantiza pasar todos los filtros ni conseguir una entrevista.",
            "trust_no_invention": "WorqAI no debería inventar experiencia. La función es reorganizar y expresar mejor lo que usted ya hizo según la vacante; la versión final siempre debe revisarse antes de enviarla.",
            "how_it_works": "Sube su CV, pega la descripción del puesto y WorqAI compara ambos. Después muestra huecos de evidencia y propone una versión adaptada que usted puede revisar y descargar.",
            "product_problem": "Gracias por avisar. Para ubicar el problema necesito saber en qué paso ocurrió, qué esperaba ver y, si puede compartirlo sin datos personales, el mensaje de error.",
            "general_interest": "Gracias por escribir. WorqAI ayuda a comparar un CV con una vacante real y adaptar la presentación de experiencia existente. Cuénteme qué tipo de puesto está buscando y le indico por dónde empezar.",
        }
    else:
        replies = {
            "pricing_or_free_access": "Yes. You can try the analysis and first tailored CV for free without a card, then start with one real vacancy.",
            "privacy_or_data": "That is an important question because CVs contain sensitive information. Review the published privacy policy and share only what is necessary; I will not claim protections that the policy does not confirm.",
            "ats_or_screening": "Yes. WorqAI compares the CV with the vacancy requirements. That can make relevance clearer, but it cannot guarantee passing every filter or getting an interview.",
            "trust_no_invention": "WorqAI should not invent experience. It reorganizes and expresses what you already did for the target role, and you should review the final version before sending it.",
            "how_it_works": "Upload the CV, paste the job description, and WorqAI compares them. It then shows evidence gaps and proposes an adapted version you can review and download.",
            "product_problem": "Thanks for reporting this. Please share which step failed, what you expected, and the error message without personal CV data if possible.",
            "general_interest": "Thanks for reaching out. WorqAI compares a CV with a real vacancy and helps present existing experience more clearly. Tell me what type of role you are targeting and I will point you to the right first step.",
        }
    return replies[intent]


def _short_reply_for(intent: str, *, spanish: bool) -> str:
    if spanish:
        replies = {
            "pricing_or_free_access": "Sí, puede empezar gratis y sin tarjeta.",
            "privacy_or_data": "Revise la política publicada y comparta solo la información necesaria.",
            "ats_or_screening": "Ayuda a alinear el CV con la vacante, sin garantizar resultados.",
            "trust_no_invention": "Adapta experiencia real; no debería inventarla.",
            "how_it_works": "Sube el CV, pega la vacante, revisa los huecos y descarga la versión adaptada.",
            "product_problem": "¿En qué paso apareció el error y qué mensaje mostró?",
            "general_interest": "Cuénteme qué puesto busca y le indico cómo empezar.",
        }
    else:
        replies = {
            "pricing_or_free_access": "Yes, you can start free without a card.",
            "privacy_or_data": "Review the published policy and share only the necessary information.",
            "ats_or_screening": "It helps align the CV with the role without guaranteeing results.",
            "trust_no_invention": "It adapts real experience; it should not invent it.",
            "how_it_works": "Upload the CV, paste the role, review the gaps, and download the adapted version.",
            "product_problem": "Which step failed, and what error did it show?",
            "general_interest": "Tell me the target role and I will suggest the best first step.",
        }
    return replies[intent]


def _follow_up_for(intent: str, *, spanish: bool) -> str:
    questions_es = {
        "pricing_or_free_access": "¿Quiere revisar el CV general o adaptarlo a una vacante específica?",
        "privacy_or_data": "¿Qué dato específico le preocupa compartir?",
        "ats_or_screening": "¿Ya tiene una vacante real para comparar?",
        "trust_no_invention": "¿Quiere ver un ejemplo antes/después basado únicamente en experiencia real?",
        "how_it_works": "¿Quiere empezar con una vacante que ya tenga guardada?",
        "product_problem": "¿Puede indicar el paso y el mensaje de error sin incluir datos personales?",
        "general_interest": "¿Qué puesto está buscando?",
    }
    questions_en = {
        "pricing_or_free_access": "Do you want to review the general CV or tailor it to one vacancy?",
        "privacy_or_data": "Which specific data are you concerned about sharing?",
        "ats_or_screening": "Do you already have a real vacancy to compare?",
        "trust_no_invention": "Would a before/after example using only real experience help?",
        "how_it_works": "Do you want to start with a vacancy you already saved?",
        "product_problem": "Can you share the step and error message without personal data?",
        "general_interest": "Which role are you targeting?",
    }
    return (questions_es if spanish else questions_en)[intent]


def _concern_summary(intent: str, message: str, *, spanish: bool) -> str:
    labels = {
        "pricing_or_free_access": "costo y acceso" if spanish else "cost and access",
        "privacy_or_data": "privacidad de datos" if spanish else "data privacy",
        "ats_or_screening": "ATS y filtros" if spanish else "ATS and screening",
        "trust_no_invention": "confianza y exactitud" if spanish else "trust and accuracy",
        "how_it_works": "funcionamiento" if spanish else "how it works",
        "product_problem": "problema de producto" if spanish else "product problem",
        "general_interest": "interés general" if spanish else "general interest",
    }
    return f"{labels[intent]}: {message[:120]}"


def _is_spanish(text: str) -> bool:
    return bool(re.search(r"[áéíóúñ¿¡]", text)) or any(
        word in text for word in ("gratis", "tarjeta", "cómo", "como", "funciona", "mensaje", "cv", "vacante")
    )
