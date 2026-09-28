#!/usr/bin/env python3
"""call-review: mediaPlayer with its built-in controls off; play, seek and marks are built in the document; the MP3 copy draws no waveform."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
from appplayer import AppPlayer  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, "captures")
BUNDLE = os.path.join(HERE, "call_review.mbd")

ap = AppPlayer()
bid = ap.install_bundle(BUNDLE)
ap.restart()
ap.open_bundle(bid)
ap.wait_text("0:00 / 0:47")
ap.wait_text("call-4418.mp3")           # the second deck lists its file once the page has laid out
ap.shot(f"{CAP}/01_at_rest.png")
ap.tap("Play")
ap.wait_text("Pause")
time.sleep(31)
ap.tap("dead air")
ap.wait_text("DEAD AIR")
ap.shot(f"{CAP}/02_playing_and_marked.png")
print("call-review: played from the document's own transport, a mark left where the tape was")
