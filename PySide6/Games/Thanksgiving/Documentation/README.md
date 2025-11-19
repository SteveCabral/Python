# Thanksgiving Family Game

This document provides a concise project-level overview for the Thanksgiving family game (PySide6). It covers architecture, key modules, runtime flow, notable implementation details, known issues/limitations, and recommended extension points so you can expand the codebase safely.

---

## Project Overview

- Purpose: A Wheel-of-Fortune–style family game implemented with PySide6. Players take turns guessing letters to reveal a phrase and score points.
- Location: project root folder `Thanksgiving/` with UI widgets in `Thanksgiving/widgets/`.
- Entry point: `main.py` — constructs the application window containing the leaderboard and game UI.

## Key Modules and Responsibilities

- `config.py` — JSON-backed configuration loader/writer; supplies `DEFAULT_CONFIG` and `game_config.json` containing `phrases` and `points`.
- `phrase_manager.py` — `Phrase` dataclass and `PhraseManager`. Validates phrase length, tracks availability, and returns the next available phrase.
- `leaderboard.py` — `LeaderboardModel` (subclass of `QAbstractTableModel`) responsible for player list, ranking, score updates, and selection state.
- `game_window.py` — `GameWindow` (PySide6 `QWidget`) composing the main gameplay area: phrase grid, letter buttons, and controls; coordinates phrase selection and scoring.
- `widgets/phrase_grid.py` — `PhraseGridWidget` responsible for splitting and rendering phrase characters into a 4-row grid.
- `widgets/letter_buttons.py` — `LetterButtonsWidget` containing letter `QPushButton`s A–Z and emitting `letter_clicked` events.

## Runtime Flow

1. `main.py` creates `MainWindow` with two panes: the left leaderboard and the right `GameWindow`.
2. Players are added via the leaderboard UI. Selecting a row marks the current player and updates the UI.
3. `Start Game`/`Next Phrase` in `GameWindow` uses `PhraseManager.next_available()` to load and display a phrase in the `PhraseGridWidget`.
4. Clicking a letter emits `letter_clicked` → `GameWindow.on_letter()` checks the phrase for occurrences, reveals letters in the grid, and updates scores via the leaderboard model.
5. Phrases should be marked unavailable once solved; the UI advances to the next available phrase.

## Notable Implementation Details & Strengths

- Clear separation of concerns: model (`LeaderboardModel`), phrase management (`PhraseManager`), and view/widgets (`PhraseGridWidget`, `LetterButtonsWidget`).
- Uses Qt model/view architecture for the leaderboard (`QAbstractTableModel`).
- Config-driven `game_config.json` makes it easy to add phrases and change per-letter points.
- Widgets are small, focused, and easily testable.

## Bugs, Limitations & Risk Areas

- Leaderboard model instance is duplicated: `MainWindow` and `GameWindow` each create a `LeaderboardModel`. As a result, score updates in `GameWindow` are not reflected in the left-hand leaderboard. This is likely unintended and should be fixed by sharing a single model instance.
- `PhraseManager.next_available()` does not mark a phrase as unavailable; `mark_unavailable()` exists but isn't invoked by the main flow, so phrases may be reused repeatedly.
- `PhraseGridWidget.display_phrase()` currently writes characters directly into labels (appearing revealed). If the intended UX is to hide letters until guessed, the display logic should be changed to show placeholders and reveal letters only after correct guesses.
- Miss penalty calculation appears incorrect: `cost = self.points_map.get(letter, 5) * 0` always yields 0 (no penalty). That likely needs correction to apply an intended negative score for misses.
- `solve()` in `game_window.py` is unimplemented — no mechanism exists for entering and evaluating full-phrase guesses.
- `split_phrase_into_rows` can overflow if a phrase exceeds the combined capacity; `PhraseManager` limits phrase length but defensive handling would help.

## Extension Points (Where to Expand)

- Share the `LeaderboardModel` between `MainWindow` and `GameWindow` by passing the same model instance into `GameWindow`'s constructor.
- Implement `GameWindow.solve()` using `QInputDialog.getText()` or a custom dialog; evaluate the guess, award points, reveal or clear phrase, and call `PhraseManager.mark_unavailable()` on success.
- Update `PhraseGridWidget` to initially display placeholders (e.g., underscores or blanks) and reveal correctly guessed letters visually; support full-phrase reveal for solved rounds.
- Fix scoring rules: implement miss penalties and configurable per-letter point values from `game_config.json`.
- Add persistence for leaderboard/high scores (e.g., `scores.json`) and optionally autosave game state between sessions.
- Add unit tests for `PhraseManager`, `config.load/save`, and `split_phrase_into_rows` to avoid regressions when changing layout logic.
- Improve UX: turn-based flow with current-player rotation, visual highlighting for current turn, and confirmation dialogs for phrase exhaustion.

## Getting Started (Developer)

1. Install dependencies (PySide6):

```bash
python -m pip install -r requirements.txt  # or `pip install PySide6`
```

2. Run the app from the `Thanksgiving/` folder:

```bash
python main.py
```

3. Suggested first changes to experiment with:
- Pass `leaderboard_model` into `GameWindow` to unify the model used by both panes.
- Implement `solve()` and call `phrase_manager.mark_unavailable()` when a phrase is solved.

## Contributing

- Follow the existing coding style: small focused modules, use of Qt signals/slots, and minimal UI logic in widgets.
- Add unit tests for behavior rather than UI-only tests where practical.

---

If you want, I can now implement one of the recommended fixes (share the leaderboard model and implement `solve()`), or create tests and CI scaffolding — tell me which and I will proceed.
