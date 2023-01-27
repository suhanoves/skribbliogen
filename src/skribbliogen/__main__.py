from __future__ import annotations

import csv

from argparse import Namespace
from pathlib import Path

from skribblio_gen.arg_parser import arg_parser
from skribblio_gen.entities import Lemma
from skribblio_gen.validators import LemmaLenValidator, PosValidator, Validator


DICTIONARY_DELIMITER = "	"
# в словаре существительные имеют почему-то литеру `s`
# мапим литеры словаря на литеры командной строки
POSES_MAP = {"n": "s"}


def config_validators(args: Namespace) -> list[Validator]:
    """Возвращает список сконфигурированных валидаторов из значений пользователя."""
    return [
        PosValidator(valid_poses=[POSES_MAP.get(pos, pos) for pos in args.poses]),
        LemmaLenValidator(
            min_length=args.lemma_min_length,
            max_length=args.lemma_max_length,
        ),
    ]


def get_lemmas(source_path: Path, validators: list[Validator]) -> list[Lemma]:
    """Получить список лемм из файла."""
    with open(Path.cwd() / source_path) as source_file:
        csv_reader = csv.reader(source_file, delimiter=DICTIONARY_DELIMITER)
        next(csv_reader)  # header

        for word, pos, frequency, *_ in csv_reader:
            lemma = Lemma(word, pos, frequency)
            if is_valid_lemma(lemma=lemma, validators=validators):
                yield lemma

    return all(validator.is_valid(lemma) for validator in validators)


def is_valid_lemma(lemma: Lemma, validators: list[Validator]) -> bool:
    """Проверяет валидность леммы переданными валидаторами."""
    return all(validator.is_valid(lemma) for validator in validators)


def sort_lemmas(lemmas: list[Lemma]) -> list[Lemma]:
    """Сортирует леммы по частоте."""
    return sorted(lemmas, key=lambda lemma: lemma.frequency, reverse=True)


def slice_lemmas(
    lemmas: list[Lemma],
    position_from: int,
    position_to: int,
    limit: int,
    delimiter: str,
) -> list[Lemma]:
    """Возвращает заданный слайс с ограничением по количеству символов."""
    result = []

    char_count = 0
    for lemma in lemmas[position_from - 1 : position_to]:
        char_count += len(lemma)
        if char_count > limit:
            break
        result.append(lemma)
        char_count += len(delimiter)
    return result


def make_lemmas_string(lemmas: list[Lemma], delimiter: str) -> str:
    """Из списка лемм создаёт строку."""
    return delimiter.join(lemma.lemma for lemma in lemmas)


def write_file(string: str, output_path: Path) -> None:
    """Записывает строку лемм в файл по указанному пути"""
    if not output_path.is_absolute():
        output_path = Path().cwd() / output_path

    with open(output_path, "w+") as output_file:
        output_file.write(lemmas_string)


if __name__ == "__main__":
    args = arg_parser.parse_args()
    validators = config_validators(args)

    unsorted_lemmas = get_lemmas(
        source_path=args.source,
        validators=validators,
    )
    sorted_lemmas = sort_lemmas(unsorted_lemmas)
    sliced_lemmas = slice_lemmas(
        lemmas=sorted_lemmas,
        position_from=args.position_from,
        position_to=args.position_to,
        limit=args.limit,
        delimiter=args.delimiter,
    )
    lemmas_string = make_lemmas_string(
        lemmas=sliced_lemmas,
        delimiter=args.delimiter,
    )
    write_file(
        string=lemmas_string,
        output_path=args.output,
    )
