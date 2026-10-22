"""synth.py - original soundtrack for a code-rendered reel, generated from scratch.

    python3 synth.py events.json out.wav

events.json: {"dur": 30.0, "bpm": 120, "events": [[t, "tick"], [t, "pop"], ...]}
Event types: tick, pop, whoosh, hit, ring, confirm.
Every sound is synthesized here; nothing is sampled, so there is nothing to license.
"""
import json, sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 48000
rng = np.random.default_rng(7)

def env(n, a=0.002, d=0.15):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
    return e

def lp(x, f): b, a = butter(2, f / (SR / 2)); return lfilter(b, a, x)
def hp(x, f): b, a = butter(2, f / (SR / 2), btype="high"); return lfilter(b, a, x)

def kick():
    n = int(SR * .35); t = np.arange(n) / SR
    f = 48 + 90 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .11) * .9

def hat():
    n = int(SR * .06)
    return hp(rng.standard_normal(n), 7000) * env(n, .0005, .012) * .12

def tick():
    n = int(SR * .05); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2200 * t) * .5 + hp(rng.standard_normal(n), 4000) * .3) * env(n, .0003, .008) * .5

def pop():
    n = int(SR * .18); t = np.arange(n) / SR
    f = 620 + 500 * np.exp(-t * 40)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .05) * .45

def confirm():
    out = np.zeros(int(SR * .45))
    for i, f in enumerate((880, 1318.5)):
        n = int(SR * .3); t = np.arange(n) / SR
        s = (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)) * env(n, .002, .09) * .28
        o = int(SR * .09 * i); out[o:o + n] += s
    return out

def whoosh():
    n = int(SR * .5); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    sweep = np.concatenate([lp(noise[:n // 2], 1800), hp(noise[n // 2:], 900)])
    shape = np.sin(np.pi * t / t[-1]) ** 2
    return sweep * shape * .22

def hit():
    n = int(SR * 1.2); t = np.arange(n) / SR
    body = sum(np.sin(2 * np.pi * f * t) for f in (110, 164.8, 220, 329.6)) / 4
    k = kick()
    return body * env(n, .002, .45) * .6 + np.pad(k, (0, n - len(k))) * .8

def ring():
    n = int(SR * .9); t = np.arange(n) / SR
    tone = (np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 480 * t)) * .5
    gate = ((t * 20) % 1 < .5).astype(float)
    return tone * gate * env(n, .005, .6) * .22

SOUNDS = {"tick": tick, "pop": pop, "whoosh": whoosh, "hit": hit, "ring": ring, "confirm": confirm}

def pad(dur, bpm):
    n = int(SR * dur); t = np.arange(n) / SR
    chords = [(110, 164.8, 220, 277.2), (98, 146.8, 196, 246.9), (87.3, 130.8, 174.6, 220), (98, 146.8, 196, 246.9)]
    bar = 4 * 60 / bpm * 2  # one chord every two bars
    out = np.zeros(n)
    for k, ch in enumerate(chords * 20):
        s, e = int(k * bar * SR), int((k + 1) * bar * SR)
        if s >= n: break
        e = min(e, n); tt = t[s:e] - t[s]
        seg = sum(np.sin(2 * np.pi * f * tt) + .25 * np.sin(2 * np.pi * f * 2.01 * tt) for f in ch) / len(ch)
        fade = np.minimum(1, np.minimum(tt / .4, (tt[-1] - tt + 1e-3) / .4))
        out[s:e] += seg * fade
    return lp(out, 1400) * .12

def place(buf, snd, t):
    s = int(t * SR)
    if s >= len(buf): return
    e = min(len(buf), s + len(snd)); buf[s:e] += snd[:e - s]

def main():
    cfg = json.load(open(sys.argv[1]))
    dur, bpm = cfg["dur"], cfg.get("bpm", 120)
    n = int(SR * dur)
    music = pad(dur, bpm)
    drums = np.zeros(n)
    beat = 60 / bpm
    start = cfg.get("drums_from", 0.0)
    duck = np.ones(n)
    k = 0
    while k * beat < dur:
        tt = k * beat
        if tt >= start:
            if k % 2 == 0: place(drums, kick(), tt)
            place(drums, hat(), tt + beat / 2)
            s = int(tt * SR); m = min(n, s + int(SR * .18))
            if k % 2 == 0: duck[s:m] = np.minimum(duck[s:m], np.linspace(.35, 1, m - s))
        k += 1
    fx = np.zeros(n)
    for t, kind in cfg["events"]:
        place(fx, SOUNDS[kind](), t)
    mix = music * duck + drums * .55 + fx
    fade = np.ones(n); fo = int(SR * .6); fade[-fo:] = np.linspace(1, 0, fo); fade[:int(SR*.05)] = np.linspace(0, 1, int(SR*.05))
    mix *= fade
    mix = np.tanh(mix * 1.4) / np.tanh(1.4)
    mix = mix / (np.abs(mix).max() + 1e-9) * 0.89
    stereo = np.stack([mix, np.roll(mix, 24)], axis=1)
    wavfile.write(sys.argv[2], SR, (stereo * 32767).astype(np.int16))
    print("wrote", sys.argv[2], f"{dur:.1f}s")

if __name__ == "__main__":
    main()
