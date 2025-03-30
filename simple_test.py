from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='mshojaei77/gemma3persian', messages=[
  {
    'role': 'system',
    'content': 'You are a precise Persian translator. Translate text into casual, everyday Persian as spoken by native speakers. Use natural Persian expressions and conversational tone rather than formal or literal translations. Your translations should sound like they were originally written in Persian. Only output the Persian translation - no explanations, notes, or original text.'
  },
  {
    'role': 'user',
    'content': '''translate this movie subtitle to Persian:

    "Attila tells me that you, too, are
alive and en route to him from Bremerhaven."

''',
  },
])

print(response.message.content)