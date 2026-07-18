import json


SYSTEM_PROMPT = """You translate subtitle text. Return JSON only as an array of objects with exactly these keys: id and translation.
Translate only the text represented by each item. Never modify IDs, timestamps, formatting, or add explanations."""


def batch_messages(units) -> list[dict[str, str]]:
    payload = [{"id": unit.id, "text": unit.source, "context": unit.context or {}} for unit in units]
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Translate these subtitle text fields and return JSON only:\n" + json.dumps(payload, ensure_ascii=False)},
    ]
