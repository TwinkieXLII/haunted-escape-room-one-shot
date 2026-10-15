# Building the print kits

All PDF generators live in `printkit/`, with one entry point at the repository root. Output names and folders stay stable.

## Setup

Use Python 3.10 or newer and Chrome/Chromium:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-print.txt
python build_pdfs.py --list
```

The renderer discovers Google Chrome on macOS or Chrome/Chromium on PATH. Override it with `--chrome /path/to/chrome` or the `PRINTKIT_CHROME` environment variable. HTML packs use Google Fonts; their existing font fallbacks apply when fonts cannot be downloaded. Generated illustrations are committed assets; rebuilding PDFs does not call an image API.

## Build commands

```sh
python build_pdfs.py all --check
python build_pdfs.py station1 station4 finale --check
python build_pdfs.py opening helpers introductions dm-guide --check
python -m unittest discover -s tests -v
```

With no target, the command builds `all`. Individual stations rebuild their own introduction and helper first; full builds create shared introductions/helpers once before station layouts. Finale builds only the finale, so use the `opening` target for the welcome scene. Errors fail the command instead of silently using a stale browser export. `--check` validates complete-pack page counts to catch pagination changes; it is not a substitute for visual inspection or a sample print.

## Layout ownership and sources

| Target | Editable sources | Outputs |
|---|---|---|
| `introductions` | `Stations/Introductions/Station_N_Player_Introduction.md` | One-page introductions in each art folder and combined introductions |
| `helpers` | `Helpers/Station_N_Helper_Cards.md` | Per-station helper HTML/PDF and combined helpers |
| `station1`, `station4` | Layout modules, approved artwork, current helper Markdown; Station 4 reaction tables come from its station Markdown | HTML component packs, component PDFs, complete PDF |
| `station2`, `station3` | Layout modules, approved artwork, introduction/helper Markdown | Component PDFs and complete PDF |
| `station5` | Armory layout module and existing PNG artwork | Player/DM HTML and component PDFs; see readiness limitation below |
| `opening` | `Finale/Opening_Print_Kit.md` | Opening HTML/PDF |
| `finale` | `Finale/Finale_Script.md`, `Finale/Finale_Print_Kit.md` | Script, gate board, card kit and complete finale PDF |
| `dm-guide` | `DM_Guide/DM_Guide.md`, crest images | Ornate guide HTML/PDF |

The opening print edition uses `Finale/Opening_Print_Kit.md` plus the staff-introduction section from `Finale/Opening_Scene.md` (inserted at `<!-- staff-introductions -->`). Edit that section once to update its printable dialogue. The rest of the opening has separate story and print editions; keep them in agreement. Station prose and art layouts likewise contain complementary instructions: review their agreement when changing rules. This consolidation does not make every document an automatic derivative of the main station files.

`printkit/common.py` owns repository paths, browser discovery, HTML-to-PDF export and PDF merging. Browser exports are validated before replacing existing PDFs; failed merges preserve the previous complete pack. `printkit/pipeline.py` owns build order and complete-pack assembly for HTML stations. `printkit/generators/` owns the individual layouts. Importing a layout module does not write files.

The old `build_*.py` commands are compatibility wrappers into the shared pipeline. They work from any current directory. Do not add new rendering logic to those wrappers. `Art/Station_5/draw_station5_art.py` is an artwork generator, not a PDF builder, and remains separate.

## Print validation

Current complete packs: Station 1 = 16 pages; Station 2 = 13; Station 3 = 14; Station 4 = 16; finale = 12. If intentional layout changes alter those totals, inspect every changed page and then update `check_outputs` and the packing guide together.

Station 5 retains the previously identified clipping on its corridor halves. Its component builder remains available for work on that issue, but the shared command does not publish a complete Station 5 pack. See `PRINT_READINESS_AUDIT.md`.

PDF generation uses existing art and layouts. Print at Actual Size / 100%, single-sided, Letter. Each station's `PRINT_AND_PACK.md` tells you which pages to cut, hide, or place in envelopes. Use `pdftoppm -png input.pdf tmp/pdfs/page` to inspect renderings after content/layout changes. Scratch files belong under ignored `tmp/`; generated deliverables stay beside their station.
