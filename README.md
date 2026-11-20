# The World Today — 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/c/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/4Quaranz/news-image-20261119/rank.svg)](https://make.fun/c/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/4Quaranz/news-image-20261119/reward.svg)](https://make.fun/c/news-image-20261119)

A one-page newspaper front page that sums up the world news of
**Thursday, 19 November 2026**, drawn entirely by `main.py` (Python 3.13,
standard library only) and written to `/output/entry.png`.

## The day in one page

Lead story — **Trump, Xi and Putin hold first three-way summit** in Shenzhen,
on the APEC sidelines: talks on nuclear risks and energy flows, a declaration
silent on Ukraine and Iran.

Also on the front page:

- **Justice — The Hague:** the UN court (ICJ) rules Myanmar committed
  genocide against the Rohingya in its 2017 crackdown — the first such
  finding against a state.
- **Markets — New York:** stocks slide for a fifth day; the S&P 500 falls
  2.02% and the Nikkei 4.68% as AI valuation fears spread.
- **Tech — AI:** Anthropic's record IPO raises about $81 billion at $83 a
  share; the stock closes up 17% on its first day.
- **War — Ukraine:** the Crimean Bridge is hit again, the third strike in
  four days; rail traffic halted.
- **Weather — India:** Cyclone Akvan nears landfall on the Andhra
  Pradesh–Odisha coast, winds to 110 km/h.
- **Space:** Voyager 1 reaches one light-day from Earth, the farthest human
  object ever flown.

Sources: AP, Reuters, BBC, UN News, DPA — all events of 19 November 2026.

## How it works

`main.py` draws the whole front page with a built-in 5×7 bitmap font and a
hand-written PNG encoder (`zlib` from the standard library). No network, no
clock, no randomness: two runs write byte-identical files.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Competition

Entry for [news-image-20261119](https://make.fun/c/news-image-20261119) on
[make.fun](https://make.fun) — "Sum up 19 November's world news in one
image". $250 in prizes, Top 50 paid.

## License

MIT — see [LICENSE](LICENSE).
