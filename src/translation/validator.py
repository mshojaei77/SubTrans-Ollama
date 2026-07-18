import json


def validate_translations(raw: str, expected_ids: list[int]) -> dict[int, str]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("Provider returned invalid JSON") from exc
    if not isinstance(payload, list) or len(payload) != len(expected_ids):
        raise ValueError("Translation count does not match input batch")
    result = {}
    for item in payload:
        if not isinstance(item, dict) or set(item) != {"id", "translation"}:
            raise ValueError("Each translation must contain only id and translation")
        if not isinstance(item["id"], int) or not isinstance(item["translation"], str):
            raise ValueError("Invalid translation item types")
        if item["id"] in result or item["id"] not in expected_ids:
            raise ValueError("Translation IDs do not match input batch")
        result[item["id"]] = item["translation"]
    if set(result) != set(expected_ids):
        raise ValueError("Translation IDs do not match input batch")
    return result


def validate_glossary(translations: dict[int, str], required: dict[int, list[str]]) -> None:
    for unit_id, targets in required.items():
        missing = [target for target in targets if target not in translations[unit_id]]
        if missing:
            raise ValueError(f"Glossary targets missing for subtitle {unit_id}: {missing}")
