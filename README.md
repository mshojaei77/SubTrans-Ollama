# Subtitle Translator

Translate movie and TV subtitles to Persian on your own computer.

You do not need to know Python, APIs, or Docker.

## Windows: the easiest way

1. Download **Subtitle Translator.exe** from the Releases page.
2. Install [Ollama](https://ollama.com/download) and leave it running.
3. Double-click **Subtitle Translator.exe**.
4. Drop your subtitle file into the window.
5. Choose the language and click **Translate**.
6. Download the translated subtitle when it is ready.

Your subtitle files and translations stay on your computer when you use Ollama.

## First-time Ollama setup

After installing Ollama, download one translation model. The app automatically finds models already installed on your computer.

If you are comfortable using a terminal, this command downloads a small model:

```text
ollama pull gemma3:4b
```

You can also use LM Studio. Open LM Studio, load a model, start its local server, and then open Subtitle Translator.

## Subtitle files supported

- `.srt`
- `.ass`
- `.ssa`
- `.vtt`
- `.lrc`

Subtitle timing, numbering, and ASS/SSA styling are preserved while the spoken text is translated.

## If no AI engine is found

The app will show a simple setup message. Either:

- open Ollama and install at least one model, or
- open LM Studio, load a model, and start its local server.

Then click **Check again**.

## If translation stops

Your completed progress is saved. Click **Continue translation** to resume instead of starting over.

## Common questions

### Can I choose another model?

Yes. The app lists models installed in Ollama or LM Studio. You can select one from the AI model list, or enter a custom model name in Advanced settings.

### Is an internet connection required?

Only to download Ollama, models, or the application. Translation itself can run offline with a local model.

### Why is translation slow?

Local AI speed depends on your computer and model size. A smaller model is faster; closing other heavy applications can also help.

### Can I translate languages other than Persian?

The current interface is optimized for Persian translation. Language options may be expanded in future releases.

### Are translations perfect?

No. AI translations can make mistakes, especially with jokes, names, accents, and ambiguous dialogue. The app preserves subtitle structure but cannot guarantee perfect wording.

## Developers

Technical setup, API usage, Docker, and local development instructions are in [docs/development.md](docs/development.md), [docs/api.md](docs/api.md), and [docs/architecture.md](docs/architecture.md).

## Privacy

With Ollama or LM Studio, subtitles are processed by the local model on your computer. If you configure an online OpenAI-compatible service, that service receives the text required for translation; check its privacy policy first.

## License

MIT License.
