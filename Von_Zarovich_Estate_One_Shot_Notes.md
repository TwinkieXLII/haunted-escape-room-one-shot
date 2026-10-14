# Von Zarovich Estate - Halloween One-Shot

## Overview
*   **Target Audience:** 6-10 players aged about 14 (range 12-16)
*   **Duration:** 1 hour
*   **Format:** 5 station-based puzzle rooms in a single space. Paired players, 10-15 mins per station, managed by a single GM.
*   **Characters:** Level 5 pre-generated characters (see `Halloween_DnD_Character_Sheets-v2.pdf`). Each ability has 3 shared USES; treat each new station as a short rest and refresh them.
*   **Win condition:** Each station awards one **Crest** (#1-#5). Seat all five in the Grand Iron Door to escape (see the finale in `Puzzle_Station_Clue_Handouts.md`).

## Where Things Live
| File | What it's for | Who sees it |
|---|---|---|
| This file | Overview, roster, station summaries, sources | DM |
| `Stations/Station_N_*.md` | Full station: DM Notes (Coaching), setup, answer key, clues, failure rules, prop specs | DM only (except items marked as player handouts) |
| `Stations/Playtests/Station_N_Playtest.md` | Simulated playtest reports (estimates, not live data) | DM |
| `Puzzle_Station_Clue_Handouts.md` | Print-ready player handouts for all five stations plus the finale | Players, when earned |
| `Mock_Playtest_Simulation_Agent_Prompt.md` | Reusable prompt for running another simulated playtest | DM |

## Character Roster & Pairs
| Station | Pair | Classes |
|---|---|---|
| 1. Library | **Fred Jones** & **Griffin / Invisible Man** | Fighter, Rogue |
| 2. Alchemist's Lab | **Quasimodo** & **Shaggy Rogers** | Artificer, Rogue |
| 3. Clockwork Observatory | **Count Dracula / Drac** & **Johnny** | Bard, Bard |
| 4. Mimic Menagerie | **Scooby-Doo** & **Murray Mummy** | Barbarian, Druid |
| 5. Collapsing Armory | **Frankenstein / Frank** & **Wayne Werewolf** | Barbarian, Barbarian |

## Puzzle Stations
Short summaries only. The station files hold the full rules, answer keys and DM coaching. Every station has the same four-clue ladder: Clue 1 (environment) at 2-3 min, Clue 2 (character sheet) at 5-6 min, Clue 3 (logic rule) at 8-9 min, and Clue 4 (bailout) held back for a critical mistake or 11:00.

### Station 1: The Library — The Crown and the Dagger
*   **File:** [Station_1_Library_Crown_and_Dagger.md](Stations/Station_1_Library_Crown_and_Dagger.md) · **Simulated solve:** 10m 40s
*   **Puzzle:** Match six stone relics (book, scythe, dagger, spear, hammer, crown) to six dusty ancestor statues. Inspecting a statue (Investigation DC 13) earns a *Telling Detail* slip. Each stain points to the tool that made it, and the statue with no stain at all gets the crown.
*   **Failure:** Any wrong placement drops every placed relic. From the second miss, a gargoyle shrieks (DC 12 Wis, 1d6 psychic). Swapping the crown and dagger releases a minor Spectre.
*   **Character Hooks:**
    *   **Fred, "Let's Split Up!"** (station ruling): Fred and his partner inspect two statues at once, both with Advantage.
    *   **Griffin, "Now You Don't" / "Mage Hand Shenanigans":** the gargoyle can't see Griffin, so he never takes the shriek. Mage Hand reaches the tall plinth.

### Station 2: The Alchemist's Laboratory — The Trickster's Coin
*   **File:** [Station_2_Alchemist_Lab_Tricksters_Coin.md](Stations/Station_2_Alchemist_Lab_Tricksters_Coin.md) · **Simulated solve:** 11m 20s
*   **Puzzle:** Ten identical vials, one a lighter counterfeit. Weigh groups on a balance scale and offer the fake to the jester altar. The DM announces each result with three set phrases.
*   **Recommended rule:** the *Trickster's Shuffle*. The fake always hides in the largest suspect group, so lucky guessing doesn't pay off. You need a suspect tracker behind the screen. The fixed answer (vial #6, the book default) is simpler but solved too fast in the playtest.
*   **Failure:** A wrong vial offered to the bowl rolls on a comedic d6 side-effect table (no damage). Weighings past the fourth cost a side-effect roll.
*   **Character Hooks:**
    *   **Quasimodo, "Esmeralda the Rat":** clears one genuine vial, leaving 9 suspects (solvable in 2 weighings with a 3-3-3 split).
    *   **Shaggy, "Iron Stomach":** no harm from tasting a vial, can end a side effect early, and powers the Clue 4 bailout belch.

### Station 3: The Clockwork Observatory — Of Gears and Gadgets
*   **File:** [Station_3_Clockwork_Observatory_Gears_and_Gadgets.md](Stations/Station_3_Clockwork_Observatory_Gears_and_Gadgets.md) · **Simulated solve:** 11m 20s
*   **Puzzle:** A plaque riddle names three constellations without naming them. The star chart shows how many stars each has, and each star is one gear tooth. Load four pegs from seven identical brass gears (three are decoys) and turn the crank. The chart's centre numeral is a sum check.
*   **Pressure:** The Clockwork Phantom strikes on a real-time tick (3:00, then every 2 min) and after every wrong crank: +5 to hit, 1d6+2. A wrong crank gives no hint about which gear was wrong.
*   **Character Hooks:**
    *   **Drac, "Look Into My Eyes!":** the phantom skips its next strike. **Bat Form** flies to the dome for Clue 2.
    *   **Johnny, "DJ Backpack":** the phantom skips its next strike. **Sick Beats** (once per station) cancels the strike from one wrong crank.
*   **Optional add-on:** *Noon Mark* (Ch 12) if the pair finishes before about 8:00.

### Station 4: The Mimic Menagerie — Wands and Keys
*   **File:** [Station_4_Mimic_Menagerie_Wands_and_Keys.md](Stations/Station_4_Mimic_Menagerie_Wands_and_Keys.md) · **Simulated solve:** 10m 50s
*   **Puzzle:** Four identical keys in four alcoves: an illusion, a mimic, an explosive construct and the real crest key. Four wands test them (Bright Light, Poison, Acid, Mage Hand). Poison and Acid have **one charge each**. Lifting a wrong key triggers it, shuffles the alcoves and recharges the wands.
*   **Shuffle:** four pre-set layouts (A-D). Start each pair on a different layout and mark the current one with a paperclip.
*   **Failure (scaled):** mimic bite +5, 1d8+2 plus 2 acid (AC 12, 15 HP). Construct blast DC 12 Dex, 2d4.
*   **Character Hooks:**
    *   **Scooby, "Scooby Snack Surge":** needs a real snack (check allergies). Scooby asks one question, "alive?" or "fake?".
    *   **Murray, "Sandstorm Shuffle":** automatically restrains the mimic for 2 rounds. **Bandage Whip** can tap pedestals (the Clue 4 bailout) or lift a key.

### Station 5: The Collapsing Armory — Corridor of the Taboo Word
*   **File:** [Station_5_Collapsing_Armory_Corridor_of_the_Taboo_Word.md](Stations/Station_5_Collapsing_Armory_Corridor_of_the_Taboo_Word.md) · **Simulated solve:** 12m 10s
*   **Puzzle:** Nobody may say the taboo word (the station file has the ruling table for variants). Five glowing ceiling words match five of eight weapon-rack tags, and the first letters of the lit weapons spell the door password. A spiked ceiling drops 1 ft per real minute from 15 ft.
*   **Failure:** Each slip rolls on a scaled d8 penalty table and locks the door for 1 minute (the book uses 5).
*   **Character Hooks:**
    *   **Frank, "Massive Shoulders":** automatic success. Holding the gargoyle boss stops the ceiling. Frank's own sheet text contains the taboo word, so watch for it.
    *   **Wayne, "Wolf Senses" + "Swarm of Pups":** hearing/smell finds the right pipe, and the pups fetch the crest through the 4-inch grate. One use lasts the whole station. (*Exhausted Dad Rage* is only Wayne's rage, not the pups.)

## Puzzle Source References
Book: *The Game Master's Book of Traps, Puzzles and Dungeons* by Jeff Ashworth (with contributors). Use this table for credits and to look up the original text in the printed book.

| Station | Puzzle used | Book chapter | Pages | Alternates noted |
|---|---|---|---|---|
| 1. Library | The Crown and the Dagger | Ch 11, Gateway Puzzles | pp. 122-141 (exact page not recorded) | Planning for War (Ch 12) |
| 2. Alchemist's Lab | The Trickster's Coin | Ch 12, Gateway Puzzles Part 2 | from about p. 142 (exact page not recorded) | Any other Ch 11/12 puzzle (Wands and Keys is now Station 4) |
| 3. Clockwork Observatory | Of Gears and Gadgets (+ Noon Mark add-on) | Ch 12, Gateway Puzzles Part 2 | from about p. 142 (exact page not recorded) | Noon Mark (Ch 12) |
| 4. Mimic Menagerie | Wands and Keys | Ch 11, Gateway Puzzles | pp. 122-141 (exact page not recorded) | The Doors Without Traps (Ch 11; its 106 HP mimic is too big) |
| 5. Collapsing Armory | Corridor of the Taboo Word | Ch 11, Gateway Puzzles | pp. 122-141 (exact page not recorded) | The Barbarian's Brilliance (Ch 11) |

**Adapted, not copied from the book:** the statue clue wording (Station 1), the vial reskin and side-effect table (Station 2), the Station 3 plaque riddle and star chart (the book's "Four in one and three in four" line is now only the Clue 4 bailout), the alcove shuffle layouts (Station 4), and the SNARE password and shortened corridor (Station 5). The Noon Mark obelisk riddle text is in the printed book.

## Scaling Notes
*   The book's numbers are tuned for higher-level parties. All damage in the station files is already scaled for Level 5 teens, and nobody should drop to 0 HP.
*   Every station targets 10-15 minutes. Simulated runs landed between 10m 40s and 12m 10s, all near the low end, so a careful pair may finish early. Station 3 (Noon Mark) and Station 4 have early-finish options.

## Open Issues / Before Game Day
*   [ ] **Schedule:** decide whether pairs play their own station at the same time or rotate through all five. "1 hour" fits one station per pair plus the intro and finale, but not five stations in a row (about 60-75 min). If pairs rotate, the character hooks only fit their home station.
*   [ ] Confirm the exact book page numbers.
*   [ ] Station 2: decide Trickster's Shuffle vs. fixed answer (#6).
*   [ ] Station 4: buy a real snack for Scooby, and check allergies.
*   [ ] Print the props from each station file's "Visual Props" section, and the handouts from `Puzzle_Station_Clue_Handouts.md`.
*   [ ] All timings come from simulated playtests. A live run with real players will be more reliable.
