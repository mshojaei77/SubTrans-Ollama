from .models import TranslationContext


class ContextBuilder:
    def __init__(self, window: int = 3):
        if window < 0:
            raise ValueError("window must be non-negative")
        self.window = window

    def build(self, subtitles, index: int) -> TranslationContext:
        previous = [line.text for line in subtitles[max(0, index - self.window):index]]
        following = [line.text for line in subtitles[index + 1:index + self.window + 1]]
        return TranslationContext(previous=previous, current=subtitles[index].text, next=following)
