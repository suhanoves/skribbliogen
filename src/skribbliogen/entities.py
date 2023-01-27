from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Lemma:
    """Класс, представляющий лемму с её основными характеристиками"""

    lemma: str
    pos: str  # часть речи
    frequency: float  # частота употребления
    validators: list = field(default_factory=list)

    def __len__(self) -> int:
        """Возвращает длину слова леммы."""
        return len(self.lemma)
