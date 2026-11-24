# Monday 23 November 2026 in One Picture

Entry for make.fun `news-image-20261123` — "Sum up 23 November's world news in one image".
$100 prize pool, 50 paid places. Free entry.

## The image

A dense newspaper front page, 1024x1024, drawn entirely with PIL:

- **Masthead** — "Monday 23 November 2026", 35 stories, 8 regions.
- **The day in UTC** — 7 timed events, 06:35 to 21:00.
- **3 lead stories** with original drawings: Wall Street roars back (Nvidia +31%),
  COP31 ends with no deal, Hormuz on edge.
- **10 numbered mid stories**, each with its own small original drawing.
- **World map** with 13 numbered pins and region counts.
- **ALSO ON MONDAY** — stories 14–35, one line each.
- **DATE CHECK** — what was deliberately left out because it happened before Monday.
- **Source legend** — CONFIRMED (2+ outlets) / OFFICIAL / REPORTED (one outlet).

## How the image is built

`gen.py` holds the data (35 stories, timeline, register, date check) and all
drawing code. Every illustration — the rising market chart, the cracked globe,
the tanker and mine, the ten mid-story scenes, the world map — is drawn from
PIL primitives for its own story; no photos, no icons, no copied assets.
`main.py` is the entrypoint: it calls `gen.build()`, writes `entry.png` to
`$MAKEFUN_OUTPUT_DIR` when set (otherwise the repo dir), and asserts the
1024x1024 size, the 1 MiB limit, and the pinned hash.

## Sources

Every story happened or was first reported on Monday 23 November 2026.
Outlets: AP, Reuters, AFP, BBC, Bloomberg, UN News, CoinDesk, UKMTO, USGS, ESA.
No facts or numbers were invented; uncertain claims are attributed in the text.

## Run

```sh
python3 gen.py        # writes entry.png in the repo
python3 main.py       # regenerates entry.png, verifies size + pinned hash
```

Deterministic: two runs produce identical bytes
(sha256 `aaa85c01a101d687ad4e1b866a5df7da7c8d2f6f3381f45c3e143c195431cee3`,
184,400 bytes). Grader-style check: run as user `nobody` with a read-only
repo copy and `MAKEFUN_OUTPUT_DIR` set — exit code 0, image written there.

## License

MIT — see LICENSE.
