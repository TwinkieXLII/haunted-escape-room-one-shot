# Haunted Escape Room One-Shot: The Von Zarovich Estate

A one-hour Halloween D&D 5e one-shot for 6–10 players aged about 12–16. Pairs of Level 5 pre-generated monster and mystery-gang characters each tackle a puzzle station inside a haunted castle, all at the same time. Every station awards a Crest and a clue. All five Crests open the Grand Gate, and then the whole group fights off the Phantom's minions, works out who's behind the haunting, and unmasks the culprit, Scooby-Doo style. It's run by a lead GM with one helper GM per station, using clue envelopes and print-and-play props.

## Start here
| File | What it is |
|---|---|
| [DM_Guide/DM_Guide.pdf](DM_Guide/DM_Guide.pdf) | **The Dungeon Master's Grimoire**: the complete ornate guide with lore, room bindings, rules, hints and solutions for all five stations, plus the finale |
| [Von_Zarovich_Estate_One_Shot_Notes.md](Von_Zarovich_Estate_One_Shot_Notes.md) | Overview: roster and pairs, station summaries, sources, open issues |
| [Stations/](Stations/) | One file per station: DM coaching notes, setup, answer key, four-clue ladder, failure rules, prop specs |
| [Stations/Playtests/](Stations/Playtests/) | Simulated playtest reports (estimates, not live-table data) |
| [Stations/Introductions/](Stations/Introductions/) | Player-facing station introductions |
| [Finale/](Finale/) | Opening scene, finale script (minion fight, accusation, unmasking), evidence and suspects, print kit |
| [Helpers/](Helpers/) | One printable kit per helper GM: helper card plus clue-envelope labels and contents |
| [Puzzle_Station_Clue_Handouts.md](Puzzle_Station_Clue_Handouts.md) | Print-ready player handouts with no answers, plus the finale gate |
| [Halloween_DnD_Character_Sheets-v2.pdf](Halloween_DnD_Character_Sheets-v2.pdf) | The 10 pre-generated character sheets |
| [BRANDGUIDE.md](BRANDGUIDE.md) | "Neon Haunted Comic" art direction and print specs |
| [Art/](Art/) | Per-station art, prompts and print-and-play packs |
| [Mock_Playtest_Simulation_Agent_Prompt.md](Mock_Playtest_Simulation_Agent_Prompt.md) | Reusable prompt for running another simulated playtest with an AI model |

## The five stations
| # | Station | Puzzle (adapted from) | Pair |
|---|---|---|---|
| 1 | The Library | The Crown and the Dagger | Fred & Griffin |
| 2 | The Alchemist's Laboratory | The Trickster's Coin | Quasimodo & Shaggy |
| 3 | The Clockwork Observatory | Of Gears and Gadgets | Drac & Johnny |
| 4 | The Mimic Menagerie | Wands and Keys | Scooby-Doo & Murray |
| 5 | The Collapsing Armory | Corridor of the Taboo Word | Frank & Wayne |

## Printing
Print the PDFs and HTML packs in `Art/Station_N/` at 100% on US Letter, with background graphics on and browser headers/footers off. Use 110 lb cardstock for cards and tokens. Rebuild PDFs with `python build_pdfs.py all --check`, or select targets such as `python build_pdfs.py station1 station4 finale --check`. See [BUILDING.md](BUILDING.md) for setup, source files and build targets. Keep anything marked **DM ONLY** behind the screen.

## Credits and notes
* Puzzle mechanics are adapted from *The Game Master's Book of Traps, Puzzles and Dungeons* by Jeff Ashworth. This repo summarizes and reworks those puzzles for this table; it doesn't reproduce the book, so pick up a copy for the originals.
* Characters are affectionate homages to *Scooby-Doo*, *Hotel Transylvania* and classic monsters. This is free, non-commercial fan content. All characters and franchises belong to their respective owners.
* Much of the art is AI-generated or procedurally drawn. Station 5's illustrations are vector stand-ins; see `Art/Station_5/Art_Generation_Prompts.md` to regenerate them.
* Station design, playtest simulations and print kits were developed with help from Claude.

## License
This project is licensed under [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/). See [LICENSE](LICENSE). You may share and adapt it for non-commercial use, with credit and a link to this repo.

The license covers only the original material here. It grants no rights to the third-party characters and franchises referenced, or to *The Game Master's Book of Traps, Puzzles and Dungeons*.
