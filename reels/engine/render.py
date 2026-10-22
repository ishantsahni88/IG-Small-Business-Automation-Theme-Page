"""Render a seek(t) HTML reel to MP4 (with its synthesized soundtrack), a cover JPG, or a contact sheet.

    python3 reels/engine/render.py <page.html> <out.mp4>                 # full render
    python3 reels/engine/render.py <page.html> <sheet.png> --sheet       # one frame per window.SHEET time

The page defines window.seek(t) and window.DUR, and optionally window.EVENTS ([[t, kind], ...]),
window.BPM, window.DRUMS_FROM (soundtrack) and window.SHEET (contact-sheet times).
Needs Playwright with Chromium, ffmpeg, numpy and scipy.
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30


def _page(p, src):
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("file://" + os.path.abspath(src))
    pg.wait_for_timeout(400)
    return b, pg


def sheet(src, out, times=None):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, pg = _page(p, src)
        times = times or pg.evaluate("window.SHEET || []")
        if not times:
            dur = pg.evaluate("DUR"); times = [round(dur * i / 12, 2) for i in range(12)]
        tmp = tempfile.mkdtemp(); files = []
        for i, t in enumerate(times):
            f = os.path.join(tmp, f"s{i:02d}.png"); pg.evaluate(f"seek({t})"); pg.screenshot(path=f); files.append(f)
        b.close()
    cols = 6
    rows = [files[i:i + cols] for i in range(0, len(files), cols)]
    args, filt, labels = [], [], []
    for f in files: args += ["-i", f]
    for r, row in enumerate(rows):
        ins = "".join(f"[{r * cols + c}]" for c in range(len(row)))
        if len(row) == 1:
            filt.append(f"{ins}pad={1080 * cols}:1920[r{r}]")
        elif len(row) < cols:
            filt.append(f"{ins}hstack={len(row)},pad={1080 * cols}:1920[r{r}]")
        else:
            filt.append(f"{ins}hstack={cols}[r{r}]")
        labels.append(f"[r{r}]")
    filt.append("".join(labels) + (f"vstack={len(rows)}" if len(rows) > 1 else "copy") + ",scale=1800:-1")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", ";".join(filt), out], check=True)
    return out


def render(src, out_mp4, cover_t=None, cover_out=None):
    from playwright.sync_api import sync_playwright
    tmp = tempfile.mkdtemp(); vid = os.path.join(tmp, "v.mp4")
    with sync_playwright() as p:
        b, pg = _page(p, src)
        dur = pg.evaluate("DUR")
        cfg = {"dur": dur, "bpm": pg.evaluate("window.BPM || 120"), "drums_from": pg.evaluate("window.DRUMS_FROM || 0"),
               "events": pg.evaluate("window.EVENTS || []")}
        if cover_out is not None:
            pg.evaluate(f"seek({cover_t if cover_t is not None else 0.6})")
            pg.screenshot(path=cover_out, type="jpeg", quality=92)
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", vid], stdin=subprocess.PIPE)
        for i in range(int(dur * FPS)):
            pg.evaluate(f"seek({i / FPS})"); ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        ff.stdin.close(); ff.wait(); b.close()
    ev = os.path.join(tmp, "ev.json"); json.dump(cfg, open(ev, "w"))
    wav = os.path.join(tmp, "a.wav")
    subprocess.run([sys.executable, os.path.join(HERE, "synth.py"), ev, wav], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", out_mp4], check=True)
    return dur


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    if "--sheet" in sys.argv:
        print("sheet", sheet(src, out))
    else:
        print("rendered", out, render(src, out), "s")
