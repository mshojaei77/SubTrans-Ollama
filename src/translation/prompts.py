import json


SYSTEM_PROMPT = """You translate subtitle text. Return JSON only as an array of objects with exactly these keys: id and translation.
Translate only the text represented by each item. Never modify IDs, timestamps, formatting, or add explanations."""


def batch_messages(units) -> list[dict[str, str]]:
    payload = []
    for unit in units:
        context = unit.context
        payload.append({"id": unit.id, "context": {
            "previous": context.previous if context else [],
            "current": context.current if context else unit.text,
            "next": context.next if context else [],
        }})
    return [
        {"role": "system", "content": SYSTEM_PROMPT + " Use previous and next lines only for pronouns, jokes, intent, and references. Do not translate context."},
        {"role": "user", "content": "Translate these subtitle text fields and return JSON only:\n" + json.dumps(payload, ensure_ascii=False)},
    ]
