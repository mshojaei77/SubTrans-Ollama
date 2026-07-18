# 🎬 Subtitle Translator — Local AI Subtitle Translation

**Translate SRT, ASS, SSA, VTT, and LRC subtitles to Persian with local AI.**

Subtitle Translator is a privacy-friendly, beginner-friendly desktop app powered by **Ollama**, **LM Studio**, and other OpenAI-compatible local AI servers. Drop in a subtitle file, choose a model, and download the translated result.

[![GitHub stars](https://img.shields.io/github/stars/mshojaei77/SubTrans-Ollama?style=for-the-badge)](https://github.com/mshojaei77/SubTrans-Ollama/stargazers)
[![GitHub release](https://img.shields.io/github/v/release/mshojaei77/SubTrans-Ollama?style=for-the-badge)](https://github.com/mshojaei77/SubTrans-Ollama/releases)
[![License](https://img.shields.io/github/license/mshojaei77/SubTrans-Ollama?style=for-the-badge)](LICENSE)

⭐ **Like the project? Star the repository to help other subtitle fans find it!**

## Why use it?

- **Local and private:** with Ollama or LM Studio, subtitle text stays on your computer.
- **Simple workflow:** upload → translate → download.
- **Multiple AI engines:** automatically discover Ollama or LM Studio models.
- **Subtitle-safe:** timestamps, numbering, ordering, and ASS/SSA styling are preserved.
- **Reliable for long files:** context, glossary, translation memory, quality checks, parallel workers, and resume checkpoints are built in.
- **Local web interface:** use it in your browser without a cloud account.

## Quick start: local web app

1. Install one local AI engine: [Ollama](#ollama-setup) or [LM Studio](#lm-studio-setup).
2. Install dependencies with `uv sync`.
3. Start the service with `uvicorn src.api.main:app`.
4. In another terminal, run `streamlit run app.py`.
5. Open the local address shown in your browser, drop in a subtitle, and click **Translate**.

## Ollama setup

1. Install [Ollama](https://ollama.com/download).
2. Leave Ollama running in the background.
3. Download a Gemma 4 model. The recommended starting point is **Gemma 4 E2B**:

   ```text
   ollama pull google/gemma-4-E2B
   ```

4. Open Subtitle Translator. It detects Ollama and lists your installed models automatically.

For a stronger GPU, try a larger Gemma 4 model such as **E4B**, **12B**, **26B A4B**, or **31B**. Larger models may improve quality but require more memory. See the [Gemma 4 model card](https://huggingface.co/google/gemma-4-E2B).

## LM Studio setup

LM Studio is a friendly alternative to Ollama with a graphical model manager.

1. Download [LM Studio](https://lmstudio.ai/).
2. Open LM Studio and search for a Gemma 4 model.
3. Download a model that fits your computer.
4. Open the **Developer** or **Local Server** tab.
5. Load the model and start the local server.
6. Leave LM Studio open, then start Subtitle Translator.

The app automatically checks LM Studio at `http://localhost:1234/v1` when Ollama is unavailable. It lists the loaded model so you can select it without copying model IDs or editing configuration files.

## Supported subtitle formats

| Format | Typical use |
| --- | --- |
| `.srt` | Movies, TV, and streaming subtitles |
| `.ass` / `.ssa` | Styled anime and advanced subtitles |
| `.vtt` | Web video and browser captions |
| `.lrc` | Timed lyrics |

The translator changes subtitle text while preserving timing and supported style metadata. AI output is not guaranteed to be perfect, especially for slang, jokes, names, and ambiguous dialogue.

## What happens during translation?

1. The subtitle file is validated and parsed.
2. Nearby lines provide context for pronouns and references.
3. Glossary terms keep names and terminology consistent.
4. Previously translated lines are reused when safe.
5. The model returns text only; subtitle structure is protected.
6. Quality checks and checkpoints make long translations safer.
7. The translated file is ready to download.

## Need help?

### “AI engine not found”

Open Ollama or LM Studio, make sure a model is installed/loaded, and click **Check again**.

### “Model not found”

Install the model in Ollama or load it in LM Studio. The app only lists models that the selected engine can currently see.

### Translation is slow

Use a smaller model, close other GPU-heavy applications, or reduce the optional batch settings in **Advanced settings**.

### Translation stopped

Your completed progress is saved. Click **Continue translation** to resume instead of starting over.

## Developers

Technical setup and architecture documentation:

- [Development guide](docs/development.md)
- [API reference](docs/api.md)
- [Architecture](docs/architecture.md)
- [Troubleshooting](docs/troubleshooting.md)

## Privacy

When using Ollama or LM Studio, translation runs locally. If you configure an online OpenAI-compatible provider, subtitle text is sent to that provider; review its privacy policy before use.

## Contributing

Bug reports, improvements, translations, and documentation updates are welcome. Open an issue or pull request on GitHub.

If Subtitle Translator saves you time, please **⭐ star the repository** and share it with someone who works with subtitles.

## Roadmap

### Available now

- One-click Windows launcher.
- Ollama and LM Studio model discovery.
- OpenAI-compatible provider support.
- SRT, ASS, SSA, VTT, and LRC parsing.
- Structure-safe translation that preserves subtitle timing and styling.
- Context-aware translation for more natural dialogue.
- Glossary and terminology consistency.
- Translation memory to avoid repeated work.
- Quality review and correction loop.
- Parallel workers for faster processing.
- Checkpoints, cancellation, and resume.
- API-backed progress and completed-file download.

### Next planned improvements

- **Automatic model download:** offer a one-click download for the recommended Gemma 4 model.
- **Better hardware guidance:** suggest Gemma 4 E2B, E4B, 12B, 26B A4B, or 31B based on available GPU memory.
- **More language pairs:** expand beyond the current Persian-focused workflow.
- **Speaker profiles:** preserve different voices for characters, narration, and technical dialogue.
- **Improved subtitle line breaking:** make translated lines easier to read on screen.
- **Whisper-based transcription:** add speech-to-text workflows for videos without subtitles.
- **Batch folders:** translate a whole season or folder while keeping filenames organized.
- **Simpler local setup:** reduce the number of commands needed to start the browser app.
- **Community glossary packs:** share terminology for anime, games, films, and technical subjects.
- **Optional cloud providers:** support remote OpenAI-compatible services for users without a local GPU.

Roadmap priorities may change based on user feedback. [Open an issue](https://github.com/mshojaei77/SubTrans-Ollama/issues) to suggest or discuss an improvement.

## License

MIT License.
