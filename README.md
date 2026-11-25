# The World in One Day — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dewikagura/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard)
[![reward](https://make.fun/badge/news-image-20261124/dewikagura/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

One image that sums up Tuesday 24 November 2026: 40 dated stories across
13 regions and 7 fields, led by Xi's purge of Shanghai party boss Chen
Jining. A UTC timeline, a pin map of where the news happened, and a
date-check audit line keep every item tied to the day.

## How it works

`main.py` (Python 3, standard library only) copies `entry.png` into the
output directory. The image itself was drawn in code with Pillow: header,
lead story, markets strip, a 36-story grid, the UTC timeline, the pin map
and the region tally.

## What is on the page

- **Lead:** Xi purges Shanghai party boss Chen Jining, probed for graft.
- **Markets:** TAIEX +8.99% on Huang's return to Nvidia; Nvidia −6% in
  New York; WTI $82.05, +2.4% on the Hormuz tanker mines.
- **Grid:** 36 more stories — the Rosstat war-dead leak, Ukraine's drones
  sinking the corvette Mercury, the Houthi strike on Riyadh's PIF Tower,
  COP31 ending with no deal, Sarkozy and Carla Bruni to stand trial,
  England's record 5,258 heat deaths, and the Cikande factory fire.
- **Timeline:** seven dated moments from 02:00 to 23:51 UTC.
- **Map:** pins for Shanghai, Riyadh, Kyiv, Paris, Jakarta and nine more
  cities, with a per-region story count.

## Run it

```sh
python3 -P -s main.py   # writes entry.png to $MAKEFUN_OUTPUT_DIR (/output)
```

## Files

- `entry.png` — the front page, 1024x1024, one day of news
- `main.py` — the entrypoint, copy-only
- `LICENSE` — MIT

Made for [make.fun](https://make.fun) · ref 6t1r9fj9
