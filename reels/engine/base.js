// base.js - shared motion helpers for seek(t) reels.
// Closed-form springs (tiny overshoot), a beat grid, and per-change spring sums,
// following the rules in the repo's verbove-268381 / koushikde-937635 prompts.
const BPM = 120, BEAT = 60 / BPM;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
// damped spring step response: 0 -> 1, ~4% overshoot, settles in ~0.45s
function spring(t, start, k = 1) {
  const x = (t - start) / (0.45 * k);
  if (x <= 0) return 0;
  const z = 0.72, w = 9.0, wd = w * Math.sqrt(1 - z * z);
  const tt = x * 0.6;
  return 1 - Math.exp(-z * w * tt) * (Math.cos(wd * tt) + (z * w / wd) * Math.sin(wd * tt));
}
// value that springs through a list of [time, target] changes (one spring per change, summed)
function track(t, keys, k) {
  let v = keys[0][1];
  for (let i = 1; i < keys.length; i++) v += (keys[i][1] - keys[i - 1][1]) * spring(t, keys[i][0], k);
  return v;
}
const mix = (a, b, p) => a + (b - a) * p;
function mixColor(c1, c2, p) {
  const h = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16));
  const a = h(c1), b = h(c2);
  return "rgb(" + a.map((x, i) => Math.round(mix(x, b[i], clamp(p)))).join(",") + ")";
}
// visibility window for content inside a morphing container:
// enters after the container starts morphing, leaves before the next morph
function win(t, a, b, fade = 0.18) { return clamp((t - a - 0.12) / fade) * clamp((b - 0.05 - t) / fade); }
function setv(el, p, dy = 26, blur = true) {
  el.style.opacity = p;
  el.style.transform = `translateY(${(1 - p) * dy}px)`;
  el.style.filter = blur && p < 1 ? `blur(${(1 - p) * 6}px)` : "none";
}
// karaoke captions from [[t, text], ...]
function captions(el, beats, t, dur, hide = []) {
  let bi = 0; for (let i = 0; i < beats.length; i++) if (t >= beats[i][0]) bi = i;
  const [bs, txt] = beats[bi], be = bi + 1 < beats.length ? beats[bi + 1][0] : dur;
  el.style.opacity = hide.includes(bi) ? 0 : 1;
  const w = txt.split(" "), lit = Math.ceil(clamp((t - bs) / ((be - bs) * .85)) * w.length);
  el.innerHTML = w.map((x, i) => `<span class="w${i < lit ? " on" : ""}">${x}</span>`).join(" ");
}
