"""Poster renderer. Three templates:
- quote     : Unhurried calm serif quote poster (1080x1350)
- statement : Small Business Automation bold statement on ink (1080x1350)
- workflow  : Small Business Automation workflow steps + before/after (1080x1350)
"""
import os
from PIL import Image, ImageDraw, ImageFont

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
W, H = 1080, 1350
_cache = {}


def F(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONTS, name), size)
    return _cache[key]


def tokens(text):
    out, hl = [], False
    for i, part in enumerate(str(text or "").split("*")):
        if i:
            hl = not hl
        out += [(w, hl) for w in part.split()]
    return out


def wrap(toks, font, maxw):
    lines, cur = [], []
    for t in toks:
        trial = " ".join(w for w, _ in cur + [t])
        if cur and font.getlength(trial) > maxw:
            lines.append(cur)
            cur = [t]
        else:
            cur.append(t)
    if cur:
        lines.append(cur)
    return lines


def balance(toks, font, maxw):
    lines = wrap(toks, font, maxw)
    if len(lines) > 1:
        target = font.getlength(" ".join(w for w, _ in toks)) / len(lines)
        while target <= maxw:
            trial = wrap(toks, font, target)
            if len(trial) == len(lines) and len(trial[-1]) > 1:
                return trial
            target += 12
    return lines


def plain(text):
    return [(w, False) for w in str(text or "").replace("*", "").split()]


def quote(b, f, n=""):
    c = b["colors"]
    im = Image.new("RGB", (W, H), c["paper"])
    d = ImageDraw.Draw(im)
    M = 110
    for size in (104, 96, 88, 80, 72, 64):
        qf = F("CormorantGaramond-Medium.ttf", size)
        ql = balance(plain(f["quote"]), qf, W - 2 * M)
        if len(ql) <= 5:
            break
    lh = int(size * 1.12)
    sf = F("CormorantGaramond-MediumItalic.ttf", 40)
    sl = balance(plain(f.get("support", "")), sf, W - 2 * M - 60)
    block = len(ql) * lh + 90 + len(sl) * 50
    y = (H - block) // 2 + 30
    d.rectangle([W // 2 - 28, y - 46, W // 2 + 28, y - 43], fill=c["accent"])
    for line in ql:
        t = " ".join(w for w, _ in line)
        d.text((W / 2, y), t, font=qf, fill=c["ink"], anchor="ma")
        y += lh
    y += 90 - (lh - size)
    for line in sl:
        d.text((W / 2, y), " ".join(w for w, _ in line), font=sf, fill=c["muted"], anchor="ma")
        y += 50
    hf = F("JetBrainsMono-Medium.ttf", 22)
    d.text((W / 2, H - 112), " ".join((b.get("handle") or b["name"]).upper()), font=hf, fill=c["muted"], anchor="ma")
    return im


def _chrome(d, b, n, dark):
    c, M = b["colors"], 88
    fg = c["paper"] if dark else c["ink"]
    sub = c["muted"] if dark else "#6B6964"
    mf = F("JetBrainsMono-Medium.ttf", 24)
    d.text((M, 70), b["name"].upper(), font=mf, fill=fg)
    if n:
        d.text((W - M, 70), n, font=mf, fill=sub, anchor="ra")
    rule = "#2A2A2A" if dark else "#CFCCC4"
    d.rectangle([M, 116, W - M, 117], fill=rule)
    d.rectangle([M, H - 120, W - M, H - 119], fill=rule)
    sf = F("JetBrainsMono-Medium.ttf", 22)
    d.text((M, H - 92), (b.get("tagline") or "").upper(), font=sf, fill=sub)
    d.text((W - M, H - 92), (b.get("handle") or "").upper(), font=sf, fill=c["accent"] if dark else c["ink"], anchor="ra")


def statement(b, f, n=""):
    c, M = b["colors"], 88
    im = Image.new("RGB", (W, H), c["ink"])
    d = ImageDraw.Draw(im)
    _chrome(d, b, n, True)
    toks = tokens(f["headline"])
    chosen = None
    for size in (112, 104, 96, 88):
        lines = wrap(toks, F("Inter-Black.ttf", size), W - 2 * M)
        if len(lines) <= 6 and len(lines[-1]) > 1:
            chosen = size
            break
    if chosen is None:
        chosen = next(s for s in (112, 104, 96, 88, 80, 72) if len(wrap(toks, F("Inter-Black.ttf", s), W - 2 * M)) <= 6)
    font = F("Inter-Black.ttf", chosen)
    lines = wrap(toks, font, W - 2 * M)
    lh = int(chosen * 1.08)
    sf = F("Inter-Regular.ttf", 38)
    sl = wrap(plain(f.get("sub", "")), sf, W - 2 * M - 40)
    block = len(lines) * lh + 70 + len(sl) * 52
    y = (H - block) // 2 - 10
    d.rectangle([M, y - 56, M + 56, y - 46], fill=c["accent"])
    for line in lines:
        x = M
        for i, (w, hl) in enumerate(line):
            word = w + (" " if i < len(line) - 1 else "")
            d.text((x, y), word, font=font, fill=c["accent"] if hl else c["paper"])
            x += font.getlength(word)
        y += lh
    y += 70
    for line in sl:
        d.text((M, y), " ".join(w for w, _ in line), font=sf, fill=c["muted"])
        y += 52
    return im


def workflow(b, f, n=""):
    c, M = b["colors"], 88
    im = Image.new("RGB", (W, H), c["paper"])
    d = ImageDraw.Draw(im)
    _chrome(d, b, n, False)
    y = 150
    if f.get("industry"):
        tf = F("JetBrainsMono-Medium.ttf", 24)
        t = str(f["industry"]).upper()
        tw = tf.getlength(t)
        d.rounded_rectangle([M, y, M + tw + 36, y + 44], radius=22, fill=c["accent"])
        d.text((M + 18, y + 22), t, font=tf, fill=c["ink"], anchor="lm")
        y += 70
    hs = 64
    hf = F("Inter-Black.ttf", hs)
    hl = wrap(plain(f["title"]), hf, W - 2 * M)
    if len(hl) > 2:
        hs = 54
        hf = F("Inter-Black.ttf", hs)
        hl = wrap(plain(f["title"]), hf, W - 2 * M)
    for line in hl:
        d.text((M, y), " ".join(w for w, _ in line), font=hf, fill=c["ink"])
        y += int(hs * 1.12)
    steps = list(f.get("steps") or [])[:5]
    box_top = H - 120 - 30 - 200
    top, bottom, k, gap = y + 40, box_top - 30, max(len(steps), 1), 22
    nh = min(96, (bottom - top - gap * (k - 1)) // k)
    total = k * nh + (k - 1) * gap
    y0 = top + (bottom - top - total) // 2
    nf = F("JetBrainsMono-Medium.ttf", 22)
    for i, s in enumerate(steps):
        yy = y0 + i * (nh + gap)
        last = i == len(steps) - 1
        d.rounded_rectangle([M, yy, W - M, yy + nh], radius=20, fill=c["accent"] if last else c["paper"], outline=c["ink"], width=3)
        d.text((M + 30, yy + nh / 2), f"{i + 1:02d}", font=nf, fill=c["ink"] if last else "#8C8A84", anchor="lm")
        fs = 36
        lf = F("Inter-SemiBold.ttf", fs)
        while lf.getlength(s) > W - 2 * M - 150 and fs > 24:
            fs -= 2
            lf = F("Inter-SemiBold.ttf", fs)
        d.text((M + 96, yy + nh / 2), s, font=lf, fill=c["ink"], anchor="lm")
        if not last:
            cx = W - M - 64
            d.rectangle([cx - 1, yy + nh, cx + 1, yy + nh + gap - 8], fill=c["ink"])
            d.polygon([(cx - 8, yy + nh + gap - 10), (cx + 8, yy + nh + gap - 10), (cx, yy + nh + gap)], fill=c["ink"])
    bx, by, bw, bh = M, box_top, W - 2 * M, 200
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20, fill=c["ink"])
    lab = F("JetBrainsMono-Medium.ttf", 20)
    d.text((bx + 30, by + 26), "WHAT CHANGES", font=lab, fill=c["accent"])
    colw = (bw - 90) / 2
    sm = F("JetBrainsMono-Medium.ttf", 18)
    tf = F("Inter-SemiBold.ttf", 28)
    for label, text, x, color in (("BEFORE", f.get("before", ""), bx + 30, "#B9B6AE"), ("AFTER", f.get("after", ""), bx + 60 + colw, c["paper"])):
        d.text((x, by + 66), label, font=sm, fill=c["muted"])
        for i, line in enumerate(wrap(plain(text), tf, colw)[:3]):
            d.text((x, by + 96 + i * 34), " ".join(w for w, _ in line), font=tf, fill=color)
    return im


TEMPLATES = {"quote": quote, "statement": statement, "workflow": workflow}


def render(brand, item, path, n=""):
    im = TEMPLATES[item["template"]](brand, item["fields"], n)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "JPEG", quality=92, subsampling=0)
    return path
