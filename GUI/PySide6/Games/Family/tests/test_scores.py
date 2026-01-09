from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scores.score_manager import score_manager


def main() -> None:
    # Create a couple of players
    alice = score_manager.ensure_player("Alice", auto_save=False)
    bob = score_manager.ensure_player("Bob", auto_save=False)

    # Record some scores
    score_manager.record_score(player_id=alice.player_id, game_id="game1", score=10, auto_save=False)
    score_manager.record_score(player_id=alice.player_id, game_id="game1", score=25, auto_save=False)
    score_manager.record_score(player_id=bob.player_id, game_id="game1", score=20, auto_save=False)
    score_manager.record_score(player_id=alice.player_id, game_id="game2", score=5, auto_save=False)
    score_manager.record_score(player_id=bob.player_id, game_id="game2", score=50, auto_save=False)

    print("Game1 leaderboard (best-per-player):")
    for player, score in score_manager.get_game_leaderboard("game1", limit=None):
        print(f"- {player.name}: {score}")

    print("\nOverall leaderboard (sum of best-per-game):")
    for player, total in score_manager.get_overall_leaderboard(limit=None):
        print(f"- {player.name}: {total}")


if __name__ == "__main__":
    main()
