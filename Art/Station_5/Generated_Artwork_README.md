# Station 5 artwork — The Collapsing Armory

## Print these
| File | What | Who sees it |
|---|---|---|
| `Station_5_Player_Print_Pack.pdf` (6 pages) | Corridor mat Sheets A + B (landscape, tape together), 8 rack tags, ceiling tracker + slider, 5 ceiling word cards, archway plaque, sump blueprint | Players (plaque at start; blueprint when they examine the grate) |
| `Station_5_DM_Print_Pack.pdf` (3 pages) | 8 d8 penalty cards, Swarm of Pups token, Armory Crest #5, rack placement and answer key | DM only (show a penalty card only when rolled; crest on solve) |

Print at 100% on Letter, background graphics on, no headers or footers. Use 110 lb cardstock for cards and tokens. Cut on the dashed lines. The `.html` versions are the editable sources; rebuild with `python3 build_station5.py`.

## How each piece was made
* **Built as HTML/SVG (exact text):** mat, rack tags, ceiling word cards, tracker, plaque, blueprint and card frames. The eight "fantasy scripts" are generated glyph sets. The same word in the same script is identical on its tag and its ceiling card. Elvish loops are closed and Sylvan loops are open (the planned decoy tell).
* **Illustrations (`penalty_1-8.png`, `pups_token.png`, `armory_crest_token.png`):** SVG art drawn by `draw_station5_art.py` in the brand palette and rendered by headless Chrome. These are **stand-ins**, flatter than the approved Station 2 painterly style. `Art_Generation_Prompts.md` has brand-guide prompts to regenerate them in an image generator using the Station 2 references. Save the new art over the same filenames and rebuild the PDFs.

| Asset | Pixels | Print size | Effective resolution |
|---|---|---|---|
| penalty_1-8.png | 1200 × 1050 | about 2.2 × 1.95 in art window | about 540 ppi |
| pups_token.png | 1200 × 1200 | 2 in circle | 600 ppi |
| armory_crest_token.png | 1200 × 1200 | 3 in circle | 400 ppi |

## Deviations from the station file's prop spec
* Rack tags and ceiling cards are **2.25 × 3 in** (spec: 2.5 × 3.5) so they fit the mat's rack slots and nine fit on one page.
* The mat is two 10 × 7.5 in landscape sheets instead of one 17 × 11 sheet. Rack slots have no numbers, as specified; the DM key gives placement.
* Penalty cards are 2.4 × 3.36 in (poker size scaled to fit three across), the same as Station 4.
* Script words drop the possessive: the Infernal tag and card spell **EXECUTIONER** (in two lines), while the English label still reads EXECUTIONER'S BLADE. The first letter (E) is unchanged.
* No player prop contains the taboo word or the password.
