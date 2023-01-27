from __future__ import annotations

import abc

from typing import Self

from skribblio_gen.entities import Lemma


class Validator(abc.ABC):
    """Базовый класс валидатора."""

    @abc.abstractmethod
    def is_valid(self, lemma: Lemma) -> bool:
        """Запуск валидации."""


class LemmaLenValidator(Validator):
    """Валидатор длины леммы."""

    def __init__(self: Self, *, min_length: int, max_length: int) -> None:
        self.min_length = min_length
        self.max_length = max_length

    def is_valid(self, lemma: Lemma) -> bool:
        return self.min_length <= len(lemma) <= self.max_length


class PosValidator(Validator):
    """Валидатор части речи."""

    def __init__(self: Self, *, valid_poses: list[str]) -> None:
        self.valid_poses = valid_poses

    def is_valid(self, lemma: Lemma) -> bool:
        return lemma.pos in self.valid_poses
