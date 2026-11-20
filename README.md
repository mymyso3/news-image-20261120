# 20 November 2026 — 4 Stories, 3 Continents, One Page — Hormuz Edition

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/mymyso3/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/mymyso3/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

Entry for [news-image-20261120](https://make.fun/bounty/news-image-20261120) on make.fun: one image that sums up the world news of Friday 20 November 2026. License: MIT (see `LICENSE`).

## The day in one image

Four stories, three continents, one page:

1. **Ukraine hits the Crimea bridge again** — Putin abandons the sea and energy ceasefire (Europe)
2. **UN court rules Myanmar genocide** — judges rule the state committed genocide against the Rohingya (Asia)
3. **Tankers burn in Hormuz** — three oil tankers hit mines and catch fire; Iran escalates attacks (Asia)
4. **Anthropic's $2tn IPO** — record debut on Nasdaq, the largest ever (North America)

`entry.png` (1024×1024) carries the date, the story and continent counts, a map with four pins on the three continents, and one card per story with its continent tag — so a viewer who missed the day can tell what happened from the image alone.

## How it works

- `draw.py` rendered `entry.png` at build time with Pillow: header, map, story cards.
- `main.py` is the runtime entrypoint (Python 3.13, standard library only): it copies `entry.png` to the output directory.
- No network. Two runs write byte-identical files.

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Referral code: `gg809aec`
