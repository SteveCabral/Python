# phrase_manager.py
from dataclasses import dataclass
from typing import List, Optional

MAX_LEN = 52

@dataclass
class Phrase:
    phrase: str
    category: str
    available: bool = True


class PhraseManager:
    def __init__(self, phrases_config: List[dict]):
        self._phrases = []
        for p in phrases_config:
            text = p.get('phrase', '').strip()
            cat = p.get('category', '').strip()
            if len(text) > MAX_LEN:
                raise ValueError(f"Phrase too long ({len(text)}): {text}")
            self._phrases.append(Phrase(text.upper(), cat.upper(), True))

    def all_phrases(self):
        return list(self._phrases)

    def next_available(self) -> Optional[Phrase]:
        for p in self._phrases:
            if p.available:
                return p
        return None

    def mark_unavailable(self, phrase: Phrase):
        for p in self._phrases:
            if p.phrase == phrase.phrase and p.category == phrase.category:
                p.available = False
                return