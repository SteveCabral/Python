from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Literal, Optional, Tuple
from uuid import uuid4

AggregateMode = Literal["best_per_game"]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Player:
    player_id: str
    name: str


@dataclass(frozen=True)
class ScoreEntry:
    entry_id: str
    player_id: str
    game_id: str
    score: int
    recorded_at: str
    meta: Dict[str, Any]


class ScoreManager:
    """Central score/leaderboard service.

    Best-practice split of responsibilities:
    - Each game computes its own score.
    - The app-level ScoreManager stores scores, computes leaderboards, and persists data.

    Data model:
    - Multiple players
    - Multiple games
    - Many score entries per (player, game)

    Leaderboards (default):
    - Per-game: best score per player
    - Overall: sum of each player's best score per game
    """

    _schema_version = 1

    def __init__(
        self,
        data_file: Optional[Path] = None,
        aggregate_mode: AggregateMode = "best_per_game",
    ) -> None:
        self._data_file = data_file or (Path(__file__).parent.parent / "scores.json")
        self._aggregate_mode: AggregateMode = aggregate_mode

        self._players: Dict[str, Dict[str, Any]] = {}
        self._scores: List[Dict[str, Any]] = []

        self.load()

    # -------------------------
    # Persistence
    # -------------------------

    def load(self) -> None:
        if not self._data_file.exists():
            self._players = {}
            self._scores = []
            return

        try:
            data = json.loads(self._data_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self._players = {}
            self._scores = []
            return

        if not isinstance(data, dict):
            self._players = {}
            self._scores = []
            return

        self._players = data.get("players", {}) if isinstance(data.get("players"), dict) else {}
        self._scores = data.get("scores", []) if isinstance(data.get("scores"), list) else []

    def save(self) -> None:
        payload = {
            "version": self._schema_version,
            "players": self._players,
            "scores": self._scores,
            "last_updated": _utc_now_iso(),
        }
        self._data_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # -------------------------
    # Players
    # -------------------------

    def list_players(self) -> List[Player]:
        players: List[Player] = []
        for player_id, pdata in self._players.items():
            name = str(pdata.get("name", ""))
            if name:
                players.append(Player(player_id=player_id, name=name))
        players.sort(key=lambda p: p.name.lower())
        return players

    def get_player(self, player_id: str) -> Optional[Player]:
        pdata = self._players.get(player_id)
        if not pdata:
            return None
        name = str(pdata.get("name", ""))
        if not name:
            return None
        return Player(player_id=player_id, name=name)

    def ensure_player(self, name: str, *, auto_save: bool = True) -> Player:
        cleaned = name.strip()
        if not cleaned:
            raise ValueError("Player name cannot be empty")

        # Case-insensitive match to avoid duplicates.
        for player_id, pdata in self._players.items():
            if str(pdata.get("name", "")).strip().lower() == cleaned.lower():
                return Player(player_id=player_id, name=str(pdata.get("name")))

        player_id = uuid4().hex
        self._players[player_id] = {
            "name": cleaned,
            "created_at": _utc_now_iso(),
        }

        if auto_save:
            self.save()

        return Player(player_id=player_id, name=cleaned)

    # -------------------------
    # Scores
    # -------------------------

    def record_score(
        self,
        *,
        player_id: str,
        game_id: str,
        score: int,
        meta: Optional[Dict[str, Any]] = None,
        auto_save: bool = True,
    ) -> ScoreEntry:
        if not self.get_player(player_id):
            raise ValueError(f"Unknown player_id: {player_id}")

        game_id_clean = game_id.strip()
        if not game_id_clean:
            raise ValueError("game_id cannot be empty")

        if not isinstance(score, int):
            raise TypeError("score must be an int")

        entry = {
            "entry_id": uuid4().hex,
            "player_id": player_id,
            "game_id": game_id_clean,
            "score": score,
            "recorded_at": _utc_now_iso(),
            "meta": meta or {},
        }
        self._scores.append(entry)

        if auto_save:
            self.save()

        return ScoreEntry(
            entry_id=entry["entry_id"],
            player_id=entry["player_id"],
            game_id=entry["game_id"],
            score=entry["score"],
            recorded_at=entry["recorded_at"],
            meta=dict(entry["meta"]),
        )

    def iter_scores(self) -> Iterable[ScoreEntry]:
        for raw in self._scores:
            try:
                yield ScoreEntry(
                    entry_id=str(raw.get("entry_id", "")),
                    player_id=str(raw.get("player_id", "")),
                    game_id=str(raw.get("game_id", "")),
                    score=int(raw.get("score", 0)),
                    recorded_at=str(raw.get("recorded_at", "")),
                    meta=dict(raw.get("meta", {}) or {}),
                )
            except Exception:
                continue

    def get_best_score(self, *, player_id: str, game_id: str) -> int:
        best: Optional[int] = None
        for entry in self.iter_scores():
            if entry.player_id == player_id and entry.game_id == game_id:
                best = entry.score if best is None else max(best, entry.score)
        return best or 0

    def _best_scores_by_player_for_game(self, game_id: str) -> Dict[str, int]:
        best: Dict[str, int] = {}
        for entry in self.iter_scores():
            if entry.game_id != game_id:
                continue
            prev = best.get(entry.player_id)
            if prev is None or entry.score > prev:
                best[entry.player_id] = entry.score
        return best

    def get_game_leaderboard(self, game_id: str, *, limit: Optional[int] = 10) -> List[Tuple[Player, int]]:
        """Return [(player, best_score)] sorted by score desc."""
        best_map = self._best_scores_by_player_for_game(game_id)
        rows: List[Tuple[Player, int]] = []
        for player_id, best_score in best_map.items():
            player = self.get_player(player_id)
            if player:
                rows.append((player, best_score))

        rows.sort(key=lambda r: (r[1], r[0].name.lower()), reverse=True)
        if limit is not None:
            return rows[:limit]
        return rows

    def get_overall_leaderboard(self, *, limit: Optional[int] = 10) -> List[Tuple[Player, int]]:
        """Return [(player, total_score)] where total_score is sum of best-per-game."""
        if self._aggregate_mode != "best_per_game":
            raise ValueError(f"Unsupported aggregate_mode: {self._aggregate_mode}")

        # Compute best score per (player, game)
        best: Dict[Tuple[str, str], int] = {}
        for entry in self.iter_scores():
            key = (entry.player_id, entry.game_id)
            prev = best.get(key)
            if prev is None or entry.score > prev:
                best[key] = entry.score

        totals: Dict[str, int] = {}
        for (player_id, _game_id), score in best.items():
            totals[player_id] = totals.get(player_id, 0) + score

        rows: List[Tuple[Player, int]] = []
        for player_id, total in totals.items():
            player = self.get_player(player_id)
            if player:
                rows.append((player, total))

        rows.sort(key=lambda r: (r[1], r[0].name.lower()), reverse=True)
        if limit is not None:
            return rows[:limit]
        return rows


score_manager = ScoreManager()
