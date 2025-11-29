# PySide6

Here is a list of PySide 6 websites I found online:


## PySide6 Websites

- [Qt for Python](https://doc.qt.io/qtforpython-6/examples/index.html)
    - Official `PySide6 documentation` website.
    - Contains examples
- [The complete PySide6 tutorial — Create GUI applications with Python](https://www.pythonguis.com/pyside6-tutorial/)
    - Useful tips on creating a GUI PySide6 application.
 

## Key Modules and Responsibilities

- `config.py` — JSON-backed configuration loader/writer; supplies `DEFAULT_CONFIG` and `game_config.json` containing `phrases` and `points`.
 - `config.py` — JSON-backed configuration loader/writer; supplies `DEFAULT_CONFIG` and `game_config.json` containing `phrases`, `points`, and `time_limit` (default `20`).
- `phrase_manager.py` — `Phrase` dataclass and `PhraseManager`. Validates phrase length, tracks availability, and returns the next available phrase.
- `leaderboard.py` — `LeaderboardModel` (subclass of `QAbstractTableModel`) responsible for player list, ranking, score updates, and selection state.
 - `leaderboard.py` — `LeaderboardModel` (subclass of `QAbstractTableModel`) responsible for player list, ranking, score updates, and selection state. New method: `reset_scores()` clears scores/played/is_selected while keeping player names so players don't need re-entering on a new game.
- `game_window.py` — `GameWindow` (PySide6 `QWidget`) composing the main gameplay area: phrase grid, letter buttons, and controls; coordinates phrase selection and scoring.
 - `game_window.py` — `GameWindow` (PySide6 `QWidget`) composing the main gameplay area: phrase grid, letter buttons, and controls; coordinates phrase selection and scoring. `Start Game` now preserves existing player names (if any) and clears their scores by calling `LeaderboardModel.reset_scores()`.
- `widgets/phrase_grid.py` — `PhraseGridWidget` responsible for splitting and rendering phrase characters into a 4-row grid.
- `widgets/letter_buttons.py` — `LetterButtonsWidget` containing letter `QPushButton`s A–Z and emitting `letter_clicked` events.
 - `widgets/letter_buttons.py` — `LetterButtonsWidget` containing letter `QPushButton`s A–Z and emitting `letter_clicked` events. Each button now shows a tooltip like `Points = <n>` indicating the per-letter value.

## Runtime Flow

1. `main.py` creates `MainWindow` with two panes: the left leaderboard and the right `GameWindow`.
2. Players are added via the leaderboard UI. Selecting a row marks the current player; the visible "Current Player" label is shown in the `GameWindow` header above the phrase grid (the leaderboard no longer shows a separate bottom label).
3. `Start Game`/`Next Phrase` in `GameWindow` uses `PhraseManager.next_available()` to load and display a phrase in the `PhraseGridWidget`.
4. Clicking a letter emits `letter_clicked` → `GameWindow.on_letter()` checks the phrase for occurrences, reveals letters in the grid, and updates scores via the leaderboard model. Each letter button's tooltip provides the points value for that letter.
5. Phrases should be marked unavailable once solved; the UI advances to the next available phrase.

## Notable Implementation Details & Strengths

- Clear separation of concerns: model (`LeaderboardModel`), phrase management (`PhraseManager`), and view/widgets (`PhraseGridWidget`, `LetterButtonsWidget`).
- Uses Qt model/view architecture for the leaderboard (`QAbstractTableModel`).
- Config-driven `game_config.json` makes it easy to add phrases, change per-letter points, and control the `time_limit` (default 20s).
- `Start Game` preserves player names and clears only scores (convenience for repeated play sessions).
- Letter buttons display tooltips indicating their point value (e.g., `Points = 5`).
- Widgets are small, focused, and easily testable.

## Bugs, Limitations & Risk Areas

- `PhraseManager.next_available()` should be checked to ensure it is marked unavailable when solved; `mark_unavailable()` exists but flow should guarantee it's called on solve.
- `PhraseGridWidget.display_phrase()` currently writes characters directly into labels; if the intended UX is to hide letters until guessed, change to placeholders and reveal logic.
- `solve()` in `game_window.py` is unimplemented — no mechanism exists for entering and evaluating full-phrase guesses.
- Defensive checks around phrase length and grid capacity are recommended to avoid layout overflow for very long phrases.

## Extension Points (Where to Expand)

- Share the `LeaderboardModel` between `MainWindow` and `GameWindow` by passing the same model instance into `GameWindow`'s constructor.
- Implement `GameWindow.solve()` using `QInputDialog.getText()` or a custom dialog; evaluate the guess, award points, reveal or clear phrase, and call `PhraseManager.mark_unavailable()` on success.
- Update `PhraseGridWidget` to initially display placeholders (e.g., underscores or blanks) and reveal correctly guessed letters visually; support full-phrase reveal for solved rounds.
- Fix scoring rules: implement miss penalties and configurable per-letter point values from `game_config.json`.
- Add persistence for leaderboard/high scores (e.g., `scores.json`) and optionally autosave game state between sessions.
- Add unit tests for `PhraseManager`, `config.load/save`, and `split_phrase_into_rows` to avoid regressions when changing layout logic.
- Improve UX: turn-based flow with current-player rotation, visual highlighting for current turn, and confirmation dialogs for phrase exhaustion.
- Keep using the existing pattern of passing `leaderboard_model` from `MainWindow` into `GameWindow` (the app already instantiates `GameWindow(self.leaderboard_model, self)` so both panes share the same model instance).
- Consider adding a `reset_scores()` test to ensure scores are zeroed while players remain after `Start Game`.
- Implement `GameWindow.solve()` and ensure `PhraseManager.mark_unavailable()` is called for solved phrases.

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

### PyGame Version

There is a separate PyGame-based recreation of this app located at the repository path:

`Thanksgiving (PyGame)/main.py`

This version reproduces the core gameplay loop (leaderboard, phrase display, letter guesses, timer) using `pygame` rather than PySide6. It reads `game_config.json` from the original `Thanksgiving/` folder so you can reuse the same phrases and per-letter points.

Install PyGame (recommended in your virtualenv):

```bash
python -m pip install pygame
```

Then run the PyGame version from the repository root (or from the `Thanksgiving (PyGame)` folder):

```bash
python "Thanksgiving (PyGame)/main.py"
```

The PyGame version supports keyboard-driven controls:
- `p` — add player (type name, Enter to commit)
- `s` — start game (keeps player names, clears scores)
- `n` — next player (resets per-player timer)
- `.` — next phrase (resets played flags)
- `A`–`Z` — guess letters
- `q` — quit

The PyGame implementation is intentionally compact and focused on recreating the gameplay without any PySide6 dependencies. Use it as a starting point if you prefer a lightweight, SDL-based frontend.

## Contributing

- Follow the existing coding style: small focused modules, use of Qt signals/slots, and minimal UI logic in widgets.
- Add unit tests for behavior rather than UI-only tests where practical.

---

If you want, I can now implement one of the recommended fixes (share the leaderboard model and implement `solve()`), or create tests and CI scaffolding — tell me which and I will proceed.
