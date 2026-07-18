import json


def judge_messages(source, translation, context=None, glossary=None):
    payload = {"source": source, "translation": translation, "context": context or {}, "glossary": glossary or []}
    return [
        {"role": "system", "content": "You are a subtitle translation reviewer. Evaluate meaning, fluency, missing or added information, glossary compliance, and style. Return JSON only with score (1-10), passed (boolean), issues (array), and suggestions (array)."},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]
