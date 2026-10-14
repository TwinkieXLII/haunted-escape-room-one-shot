# Von Zarovich Estate — Visual Brand Guide & Art Bible
*Official Art Direction: Neon Haunted Comic (8.5" x 11" Print & Play)*

---

## 1. Core Visual Identity: "Neon Haunted Comic"

This brand guide establishes the strict art direction for all visual assets generated for the **Von Zarovich Estate Halloween One-Shot**.

### Aesthetic Philosophy
*   **The Inspiration:** *Scooby-Doo! Mystery Incorporated* meets *Hotel Transylvania* with a touch of *Gravity Falls*.
*   **The Vibe:** High-energy animated Halloween heist. It balances gothic castle atmosphere with bold, expressive character art, vibrant supernatural neons, and dynamic comic-book ink outlines.
*   **The Audience:** 12–16-year-old boys. Visuals must be immediately readable across a cluttered game table, tactile, humorous, and exciting (avoiding dull brown/grey realism).

```
┌────────────────────────────────────────────────────────────────────────┐
│                   THE "NEON HAUNTED COMIC" DNA                         │
├───────────────────┬────────────────────────────────────────────────────┤
│ Inking & Lines    │ Heavy, bold black dynamic outlines (2px–4px scale) │
│                   │ with clean vector-cel shading and sharp angles.    │
├───────────────────┼────────────────────────────────────────────────────┤
│ Backgrounds       │ Deep midnight hues (#0E0B16), deep plum (#2C1438),  │
│                   │ and gothic stone grey (#2B2D42).                   │
├───────────────────┼────────────────────────────────────────────────────┤
│ Supernatural Glow │ Hyper-saturated pop colors: Toxic Slime Green      │
│                   │ (#39FF14), Electric Cyan (#00F0FF), Hot Magenta    │
│                   │ (#FF007F), and Pumpkin Amber (#FF7700).            │
├───────────────────┼────────────────────────────────────────────────────┤
│ Lighting          │ Dramatic rim-lighting, glowing magical eyes,       │
│                   │ bubbling chemical steam, and expressive silhouettes│
└───────────────────┴────────────────────────────────────────────────────┘
```

---

## 2. Official Color Palette (RGB Hex; printer conversion varies)

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   #0E0B16   │   #2C1438   │   #39FF14   │   #00F0FF   │   #FF007F   │
│  Midnight   │  Barovian   │  Toxic Ecto │  Spectral   │  Vampire    │
│    Void     │    Plum     │    Green    │    Cyan     │   Magenta   │
│ [Background]│  [Shadow]   │  [Potions]  │   [Magic]   │  [Hazards]  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   #FF7700   │   #FFD700   │   #E0D7EC   │   #FFFFFF   │   #1A1A1A   │
│  Jack-o'-   │  Cursed     │ Ghost-Paper │  Crisp      │  Pure Ink   │
│   Lantern   │   Gold      │  Parchment  │  Highlight  │   Border    │
│  [Warning]  │ [Artifacts] │  [Handouts] │  [Specular] │  [Linework] │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

---

## 3. Typography & Text Standards

*   **Header / Card Titles:** *Bangers*, *Creepster*, or *Boogaloo* (Bold, slightly irregular, comic-horror lettering with a thin black stroke and white/gold fill).
*   **Riddles & Flavour Text:** *Patrick Hand* or *Anime Ace 2.0* (Highly legible handwritten comic lettering, all-caps or clean mixed case).
*   **UI Labels & Numbers:** *Montserrat Black* or *Komika Axis* (Chunky sans-serif for numbers `1` through `10`, `VIAL #`, or `PEG #`).

---

## 4. Print & Play Technical Specifications (Home Color Printer)

All assets must be formatted to print seamlessly on standard **8.5" x 11" (US Letter)** paper and cardstock using consumer inkjet or laser printers.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      8.5" x 11" SHEET LAYOUT RULES                     │
├───────────────────────┬────────────────────────────────────────────────┤
│ Standard Paper Stock  │ 110 lb (300 gsm) white cardstock for cards,    │
│                       │ tokens, and standees; 24 lb paper for handouts.│
├───────────────────────┼────────────────────────────────────────────────┤
│ Resolution            │ 300 ppi target; report actual pixels / printed inches │
├───────────────────────┼────────────────────────────────────────────────┤
│ Margins & Safe Area   │ 0.5" (12.7 mm) white border on all four outer  │
│                       │ edges to prevent printer edge clipping.        │
├───────────────────────┼────────────────────────────────────────────────┤
│ Cut Guides & Gutters  │ 1 pt faint grey cutting guides with 2 mm       │
│                       │ gutters between adjacent cards.                │
├───────────────────────┼────────────────────────────────────────────────┤
│ Card Sizes on Sheet   │ • Poker Size (2.5" x 3.5"): 6 cards per sheet  │
│                       │ • Tarot Size (2.75" x 4.75"): 4 cards per sheet│
│                       │ • Standees (2" x 4" folded): 6 per sheet       │
│                       │ • Round Tokens (2.5" to 3"): up to 6 per sheet  │
├───────────────────────┼────────────────────────────────────────────────┤
│ Ink-Density Control   │ Solid black backgrounds should use #1A1A1A     │
│                       │ with printer ink settings checked; RGB is not ink coverage.  │
└───────────────────────┴────────────────────────────────────────────────┘
```

---

## 5. Master AI Image Generator Prompt Recipe

When directing an AI image generator (Midjourney v6, DALL-E 3, Flux), use this exact prompt structure:

```text
[STYLE WRAPPER]: 
"Stylized animation cel art, Scooby-Doo Mystery Incorporated meets Hotel Transylvania, bold ink outlines, vibrant cel shading, dark midnight background (#0E0B16) with dramatic high-contrast glowing neon highlights, clean dynamic graphic design, sharp comic book composition, crisp print-oriented artwork; verify actual pixels and print size after generation."

[SUBJECT & COMPONENT SPECIFICATION]: 
{Describe the specific item, layout, and visual tells from the Station guides below}

[COLOR & LIGHTING DIRECTIVE]: 
"Dominated by deep purples and midnight blues, punctuated by glowing toxic green (#39FF14) and electric cyan (#00F0FF) magical accents, high table readability."

[NEGATIVE PROMPT / AVOID]: 
"Photorealistic, 3D CGI render, generic anime, blurry edges, dull desaturated brown-grey colors, low contrast, unreadable decorative gibberish text, modern plastic."
```

---

## 6. Station-by-Station Visual Asset Roster

### Station 1: The Library (The Crown & The Dagger)
*   **Sheet 1 (Ancestor Standees):** 6 fold-up standees (Victoria, Alexi, Teresa, Valerius, Borislav, King Barov) with neutral art and first names only; keep telling details on separate inspection slips as prescribed by the current station file.
*   **Sheet 2 (Relic Tokens & Handouts):** 6 punch-out square relic tokens (Book, Scythe, Dagger, Spear, Hammer, Crown) + Reading Table Inscription Handout with glowing purple rune borders + Archive Crest #1.

### Station 2: The Alchemist’s Lab (The Trickster’s Coin)
*   **Sheet 1 (The 10 Vials):** 10 potion bottle cards (2" x 3"). All ten use identical amber bottles, opaque purple liquid, black seals and lighting. Only their numbers differ; never highlight vial #6.
*   **Sheet 2 (The Balance Scale Playmat):** 11" x 8.5" horizontal mat with glowing neon outlines for `LEFT PAN` and `RIGHT PAN` and a bat-shaped needle gauge.
*   **Sheet 3 (Standee & Penalty Cards):** 5" x 7" Trickster Jester Altar standee with glowing green eyes + 6 cartoon penalty cards (Bubble Burps, Helium Voice, Glow, Sneeze, Heavy Boots, Tingling Fingers) + Alchemist Crest #2.

### Station 3: The Observatory (Of Gears & Gadgets)
*   **Sheet 1 (Vault Door Board):** 11" x 8.5" brass vault door with Pegs 1, 2, 3, 4 framed in glowing constellation rings.
*   **Sheet 2 (Cogwheel Tokens & Standee):** 7 cutout gears with exaggerated, countable teeth (4, 7, 7, 3 and decoys 5, 6, 8, all in the same celestial brass finish) + Clockwork Phantom standee + Observatory Crest #3.

### Station 4: The Mimic Menagerie (Wands & Keys)
*   **Sheet 1 (The 4 Alcove Display Cards):** 4 cards (5" x 7") reuse ONE identical silver wolf-key alcove illustration. Only labels I, II, III, IV differ. No contents, odd shadows, saliva, fuses or other tells appear before testing.
*   **Sheet 2 (The 4 Testing Wands & Mimic Standee):** 4 bookmark wands (Sunbeam, Poison Skull, Acid Droplet, Spectral Hand) + silver-key mimic standee with purple tongue + Menagerie Crest #4.

### Station 5: The Collapsing Armory (Corridor of the Taboo Word)
*   **Sheet 1 (Armory Mat & Ceiling Tracker):** 11" x 17" (or two 8.5" x 11" halves) corridor battlemat with side ceiling tracker (15 ft down to 0 ft CRUSH) and spiked slider token.
*   **Sheet 2 (Blueprint, d8 Cards & Tokens):** Blueprint cross-section of 4-inch grate + 8 cartoon d8 penalty cards (Arrows, Vines, Heat Metal, Blinding, Flame, Grease, Blade, Ceiling Surge) + Swarm of Werewolf Pups token + Armory Crest #5.

### Centerpiece: The Grand Gate of Castle Ravenloft
*   **The Assembly Board (11" x 8.5"):** A massive gothic archway with five circular recessed sockets. When all 5 Crest tokens (Library, Alchemy, Observatory, Menagerie, Armory) are placed, their interlocking teeth click together in a glowing circle, revealing the escape door!


## 7. Approved reference set — Station 2, approved 2026-10-14

The user approved these actual images as the visual standard. Use their appearance, not just the cartoon franchise names, to reproduce the style.

| Reference | What to match |
|---|---|
| [Vial cards](Art/Station_2/numbered_vials_sheet.png) | Ornate gold scrollwork, black contours, tactile amber glass, identical repeated props, generous legible number plates |
| [Balance mat](Art/Station_2/balance_scale_mat.png) | Usable open play areas surrounded by dense gothic scenery, brass bat ornament, cyan/green edge light |
| [Altar](Art/Station_2/tricksters_altar_standee.png) | Exaggerated carved silhouette, expressive face, smoky green magic, white cutting outline |
| [Crest](Art/Station_2/alchemist_crest_token.png) | Antique silver relief, engraved detail, plum recesses, cyan halo, circular puzzle-tooth rim |
| [Penalty cards](Art/Station_2/comedic_penalty_cards.png) | Expressive comic mishaps, confident ink, rich cel shading, plum card frames |
| [Clue sheets](Art/Station_2/parchment_handouts.png) | Pale singed parchment, restrained marginal drawings and seals, dark readable body lettering |

### Reproduction requirements
- Use the built-in image generator for illustrated art. View the relevant approved reference and supply it as a style reference, explicitly requesting a NEW artifact rather than editing the original.
- Retain the rich engraved, scratched and painted surface detail seen in Station 2. Bold animation outlines coexist with layered metallic highlights and textured shadows. Do not simplify into flat clip art or generic minimalist vectors.
- Base palette: midnight black/plum; warm antique gold and silver; limited saturated cyan, green and magenta glow. Pale parchment provides strong text contrast.
- Use blackletter or comic-gothic headings where readable. Body text may use a clear serif like the approved parchment; do not force every paragraph into display lettering.
- For hidden-identity puzzles, reuse one master image exactly. Add labels in the print layout; separately generated near-matches are not interchangeable.
- Keep reveals, solutions, shuffle tables and coaching separate from starting player props. Give progressive clues only at their stated trigger.
- Copy exact mechanics, names and clue wording from the current station file. Never encode the answer by color, border, wear, glow, orientation or background details.
- Generate one asset per call, save named PNGs in Art/Station_N, and preserve a prompt manifest including reference paths. Build printable layouts using those images with reliable HTML text for rules and labels.
- Verify counts, numerals, text, visibility rules, dimensions and print margins. Record actual resolution; never claim 300 ppi solely because the prompt requested it.
- Letter pages have 0.5-inch margins. Fit assets into the 7.5 by 10 inch printable area, with cutting gutters. A 5 by 7 inch card uses its own page; three 2.5-inch-wide cards need narrower cards or smaller gutters to fit.
- The current station file governs puzzle behavior when older art rosters disagree.

### Reusable prompt opening
“Create a NEW tabletop artifact in the approved Station 2 Neon Haunted Comic style. The attached image is a style reference only. Match its ornate gothic framing, rich engraved metal textures, confident black comic contours, layered cel shading, deep midnight/plum recesses and saturated cyan/green/magenta rim light. Keep the subject readable and the game interaction area uncluttered. [SUBJECT]. [EXACT TEXT]. [HIDDEN INFORMATION CONSTRAINTS]. [ASPECT RATIO]. No added answer clues, no watermarks.”
