# call-review

MediaPlayer with its built-in controls off; play, seek and marks are built in the document; the MP3 copy draws no waveform.

Article: `mediaplayer-custom-transport` (not yet published)

## What is here

- `call_review.mbd/` — the app as a folder of JSON: `manifest.json` and the pages under `ui/`. No build step.
- `captures/` — screenshots taken from AppPlayer by `verify.py`.
- `verify.py`, `verify.sh` — the check.

## Open it in AppPlayer

Install the folder `call_review.mbd`.

## Verify

```bash
bash verify.sh
```

Needs AppPlayer with the debug MCP on (see `tools/README.md`). The script builds what needs building, drives the player through the screens above, asserts the claim at the top of this file, and writes `captures/`.
