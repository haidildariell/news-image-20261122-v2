# Sunday 22 November 2026 — The Day in World News

[![Competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/haidildariell/news-image-20261122-v2/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/haidildariell/news-image-20261122-v2/reward.svg)](https://make.fun/bounty/news-image-20261122)

Bounty: https://make.fun/bounty/news-image-20261122

## What this is

A single 1024×1024 page that sums up **Sunday 22 November 2026** in world
news: **35 stories across 7 regions**, drawn as a warm broadsheet front page.

- A navy masthead with the date in giant serif type
- A "day in numbers" strip (400 drones, 110 missiles, 11 killed in Sinaloa,
  14 flights cancelled, 10,000 forest staff covered, 19 years in the Pannun case)
- Four lead cards with big-word banners — **400 DRONES** over Kyiv,
  **GULF WIDENS**, COP31 **DEADLOCK**, **PROVOCATION** on the NATO border —
  each with a source chip and a CONFIRMED / REPORTED status chip
- Eight mid briefs with bold place lead-ins, a dotted "WHERE IT HAPPENED"
  map with 12 numbered pins, and a 23-line "ALSO ON SUNDAY" digest
- A DATE CHECK box that states the date discipline out loud: the Peru 6.9
  quake (Friday 20 Nov local, reported 21 Nov) was discarded as off-day

## This v2 rebuild

The previous version carried 42 stories and the page collapsed under its
own density. This rebuild is a legibility pass: 35 stories, larger type,
shorter digest lines (one printed line each), and pins spread so every
number stays readable. All rendering code was written fresh for this
version.

## How it runs

- `build_image.py` — the renderer (Python + Pillow). Reads
  `stories_20261122.json`, draws the page, writes `entry.png`.
  Deterministic: repeated runs produce a byte-identical PNG.
- `main.py` — the judged entrypoint. Stdlib only; copies the pre-rendered
  `entry.png` to `/output/entry.png`.
- `SOURCES.md` — the wire source behind every story on the page.

## License

MIT — see `LICENSE`.
