#!/usr/bin/env python3
"""Synthesise the recordings this sample reviews.

The call is generated rather than recorded for one reason: a sample that ships
a real customer call cannot ship at all. Everything the screen claims about the
audio has to be true of these files, so they are built to be true — telephone
band, 8 kHz mono, and a six-second stretch of dead air where the article says
there is one.

    python3 make_assets.py

Writes call_review.mbd/assets/. Requires ffmpeg only for the mp3 twin.
"""

import math
import os
import random
import struct
import subprocess
import wave

RATE = 8000                      # telephone band — what a call recorder keeps
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "call_review.mbd", "assets")

# The call, as the screen describes it: 47 seconds, dead air from 0:26 to 0:32.
LENGTH = 47.0
DEAD_FROM, DEAD_TO = 26.0, 32.0


def speech_like(t, seed):
    """A voiced burst: a low fundamental plus formants, not a pure tone.

    A pure sine would draw a flat rectangle in the waveform and prove nothing
    about amplitude. Real speech is loud in bursts and near-silent between
    syllables, and that is the shape the reviewer reads.
    """
    rnd = random.Random(seed)
    f0 = rnd.uniform(95, 165)                       # speaker's pitch
    syllable = 0.5 + 0.5 * math.sin(2 * math.pi * 3.7 * t + seed)
    body = (
        math.sin(2 * math.pi * f0 * t)
        + 0.5 * math.sin(2 * math.pi * f0 * 2.4 * t)
        + 0.25 * math.sin(2 * math.pi * f0 * 4.1 * t)
    )
    return body * (syllable ** 2)


def build_call():
    """Two speakers taking turns, with the dead air in the middle."""
    frames = bytearray()
    turn_edges = [0.0, 4.5, 9.0, 14.5, 19.0, 26.0, 32.0, 37.5, 43.0, LENGTH]
    n = int(LENGTH * RATE)
    for i in range(n):
        t = i / RATE
        if DEAD_FROM <= t < DEAD_TO:
            # Dead air is not digital silence — a line still carries some hiss.
            sample = random.uniform(-0.004, 0.004)
        else:
            turn = sum(1 for e in turn_edges if e <= t)
            gain = 0.62 if turn % 2 else 0.40      # agent louder than caller
            sample = speech_like(t, turn) * gain * 0.28
        frames += struct.pack("<h", int(max(-1.0, min(1.0, sample)) * 32767))
    return bytes(frames)


def build_chime():
    """The mark confirmation — a quarter second, two notes, fading out."""
    frames = bytearray()
    n = int(0.25 * RATE)
    for i in range(n):
        t = i / RATE
        pitch = 880.0 if t < 0.10 else 1174.7
        env = math.exp(-6.0 * t)
        frames += struct.pack("<h", int(math.sin(2 * math.pi * pitch * t) * env * 0.5 * 32767))
    return bytes(frames)


def write_wav(path, payload):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(payload)


def main():
    os.makedirs(OUT, exist_ok=True)
    random.seed(4417)

    call = build_call()
    wav_path = os.path.join(OUT, "call-4417.wav")
    write_wav(wav_path, call)

    write_wav(os.path.join(OUT, "mark.wav"), build_chime())

    # The same call in a compressed container. The screen puts the two side by
    # side because the waveform slot behaves differently for them, and a claim
    # about that difference needs both files present.
    mp3_path = os.path.join(OUT, "call-4418.mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
         "-codec:a", "libmp3lame", "-b:a", "32k", "-ar", "8000", mp3_path],
        check=True,
    )

    for name in ("call-4417.wav", "call-4418.mp3", "mark.wav"):
        p = os.path.join(OUT, name)
        print(f"  {name:16} {os.path.getsize(p):>9,} bytes")


if __name__ == "__main__":
    main()
