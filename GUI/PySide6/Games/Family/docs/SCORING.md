# Scoring & Leaderboards

This app supports **multiple players** and computes leaderboards across **multiple games**.

## Best-Practice Responsibility Split

- **Each game** is responsible for *calculating* a score for the current play session.
- The **main app** is responsible for:
  - Player management (who is playing)
  - Persisting results
  - Computing leaderboards
  - Combining scores across games

This keeps game modules small and makes the leaderboard consistent across every game.

## Data Model

- Players are stored with stable IDs.
- Each completed play creates a score entry: `(player_id, game_id, score, timestamp, meta)`.

## Leaderboards

- **Per-game leaderboard**: best score per player for that game.
- **Overall leaderboard**: sum of each player’s best score for every game.

(That overall metric matches a typical “family night” setup: you want to know who is strongest across all games, not just who played the most rounds.)

## How Games Submit Scores

Games receive an optional `score_reporter` callback. When a game finishes a round, it calls:

- `score_reporter(game_id, score, meta)`

The main UI decides which player is active and records the score.

`game_id` is typically the module name from `games/` (e.g., `game1`).

In the current UI, the active player is selected on the **Players** screen (second item in the left navigation).

## Leaderboard Screen

The app includes a dedicated **Leaderboard** screen (first item in the left navigation) with:

- **Overall** leaderboard (sum of best-per-game)
- **Per-Game** leaderboard (best score per player)

## Persistence

Scores (and the player registry) are stored in `scores.json` in the project root (next to `user_prefs.json`).

`user_prefs.json` is used for lightweight user/UI state (e.g., current player selection), not for the leaderboard data.
