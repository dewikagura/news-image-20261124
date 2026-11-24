# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dewikagura/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dewikagura/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-image front page summing up 24 November 2026's world news, for the
make.fun competition `news-image-20261124`. This is version 1, built in the
early morning (WIB) from the news known so far; the image will be rebuilt
with the full day's news in the evening.

## What the image shows

Masthead **WORLD NEWS** with the date **Tuesday, 24 November 2026**, then:

- **LEAD — CONFLICT: Russia warns Estonia of 'open war'.** Moscow accuses
  Tallinn of 'hostile actions' after Estonia decides to shut its Russia
  border crossings from Dec 1. Stat panel: 6 months, the length of the
  closure; crossings shut Dec 1.
- **MARKETS: Nvidia: Huang is back, shares soar ~30%.** Board reinstates
  the CEO 11 days after he quit; Nvidia adds ~$1 trillion in value in
  a day.
- **INCIDENT: 89 hurt as 'unknown substance' fills arena.** 12,000
  evacuated from Don Toliver's Manchester show; his London date is
  postponed.
- **CLIMATE: COP31 fallout: first failure since 2009.** Blame game after
  Antalya ends with no deal; disputes move to COP32 in Ethiopia.
- **CONFLICT: Ukraine's naval war spreads overseas.** Corvette Merkury
  sunk off Libya; a Russian freighter is hit in the Baltic.
- **POLITICS: EU proposes sweeping new Russia sanctions.** Banks, crypto
  and sports events targeted in the next package.
- **JUSTICE: Prince Andrew 'bribe' claim in court.** Ex-prince 'took
  £750,000 to help a Turkish heiress', the High Court is told.
- **IN BRIEF:** Iran — Trump warns Tehran of a 'very traumatic' outcome
  if no nuclear deal is struck. Armenia — Pashinyan unveils a draft
  constitution, key to a peace deal with Azerbaijan. Spain — Top court
  drops all charges against Catalan separatist leader Puigdemont.

## How the image was made

`tools/draw.py` draws the front page with Python PIL (DejaVu + Noto Serif
Display fonts) — crisp exact text, no AI-generated imagery. Re-run it to
regenerate `entry.png`:

```sh
python3 tools/draw.py
```

## Fact notes (verified 24 Nov 2026 against Reuters, BBC, CNN, AP, LA Times, The Times, WSJ)

- The news day was young when this version was built (early morning WIB):
  several stories happened 21–23 Nov and were confirmed / developed on
  24 Nov (the Russia–Estonia warning and the Nvidia reinstatement on Mon
  23 Nov; the Manchester incident on Sun 22 Nov, with the London
  postponement and the 89-symptoms police update on Tue 24 Nov). Nothing
  shown predates 21 Nov 2026.
- Manchester: the incident was Sun 22 Nov ~22:00 GMT at Co-op Live during
  a Don Toliver concert; 12,000+ evacuated, 1 person hospitalised. The
  "89 hurt" figure is the latest police update (The Times, 24 Nov): 89
  people displayed symptoms, 1 woman taken to hospital, 88 given dry
  decontamination at the scene. The London O2 show, due Tue 24 Nov, was
  postponed to 15 Dec. Earlier reports said 50+ assessed — the 89 figure
  supersedes them.
- Nvidia: board reinstated Jensen Huang as CEO on Mon 23 Nov, 11 days
  after he resigned; shares rose ~30% in early trading and over 32% in
  afternoon trades; WSJ: Nvidia added nearly $1 trillion in market value
  in one day, the most by any company in one day in history.
- COP31: the Antalya summit ended Sun 22 Nov without a deal — the first
  climate summit since Copenhagen 2009 to fail to reach a final agreement
  (Reuters). Disputes move to COP32 in Ethiopia.
- Ukraine naval war: the corvette Merkury was sunk at Benghazi, Libya, on
  Sun 22 Nov (Zelensky: seven naval drones; a second vessel hit offshore);
  the freighter Sparta II was hit by drones on Sat 21 Nov in the Gulf of
  Finland, 16 crew evacuated.
- EU sanctions: the proposal (banks, crypto, sports events) is as reported
  by the LA Times; no package details beyond that are shown.
- Prince Andrew: the £750,000 figure is an alleged bribe as told to the
  High Court on Mon 23 Nov, not an established fact.
- ICJ's Myanmar genocide ruling (19 Nov) was NOT used: it predates the
  news window by five days.

## Run it

```sh
python3 main.py            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` is standard library only and just copies `entry.png` (1024×1024
PNG, ≤1 MiB), then reads the copy back and checks it byte-for-byte. It
runs twice with identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=6t1r9fj9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
