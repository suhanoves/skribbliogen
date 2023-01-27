from __future__ import annotations

import argparse

from pathlib import Path


arg_parser = argparse.ArgumentParser(
    prog="Генератор слов для игры Scribble",
    description="Позволяет получить список слов из частотного словаря Русского языка",
    epilog="Text at the bottom of help",
)

arg_parser.add_argument(
    "-s",
    "--source",
    type=Path,
    metavar="FILE_PATH",
    default="skribblio_gen/dictionaries/ru.csv",
    help=(
        "Путь до источника частотного словаря."
        "По умолчанию используется поставляемый со скриптом файл "
        "`ru.csv` из папки `./dictionaries`."
        "Файл словаря должен представлять собой csv файл из трёх колонок "
        "| лемма | часть речи | частотность |, разделённых табуляцией. "
        "Используемые сокращение частей речи смотри в аргументе --poses."
    ),
)
arg_parser.add_argument(
    "-o",
    "--output",
    type=Path,
    metavar="FILE_PATH",
    default="./words.txt",
    help="Путь до файла, в котором сохранятся сгенерированные слова.",
)
arg_parser.add_argument(
    "-p",
    "--poses",
    type=str,
    nargs="*",
    choices=["n", "v", "a", "adv"],
    default=["n"],
    help=(
        "Часть речи, где:"
        "n (noun) - существительное;"
        "v (verb) - глагол;"
        "a (adjective) - прилагательное;"
        "adv (adverb) - наречие."
    ),
)
arg_parser.add_argument(
    "--min",
    dest="lemma_min_length",
    type=int,
    metavar="INT",
    default=4,
    help="Минимальная длина слова. Слова с меньшей длиной будут игнорироваться",
)
arg_parser.add_argument(
    "--max",
    dest="lemma_max_length",
    type=int,
    metavar="INT",
    default=12,
    help="Минимальная длина слова. Слова с большой длиной будут игнорироваться",
)
arg_parser.add_argument(
    "-f",
    "--from",
    dest="position_from",
    type=int,
    metavar="INT",
    default=1,
    help=(
        "Стартовая позиция в списке слов, отсортированном по уменьшению частотности."
        "В вывод попадут слова начиная с этой позиции. По умолчанию 1"
    ),
)
arg_parser.add_argument(
    "-t",
    "--to",
    dest="position_to",
    type=int,
    metavar="INT",
    default=5000,
    help=(
        "Финальная позиция в списке слов, отсортированном по уменьшению частотности."
        "В вывод попадут слова до позиции. По умолчанию 5000"
    ),
)
arg_parser.add_argument(
    "-l",
    "--limit",
    type=int,
    metavar="INT",
    default=20000,
    help=(
        "Ограничение по количеству символов, которые можно вывести в сгенерированном"
        " файле. По умолчанию 20 000 (определено игрой)"
    ),
)
arg_parser.add_argument(
    "-d",
    "--delimiter",
    type=str,
    metavar="SYMBOL",
    default=",",
    help="Разделитель слов в сгенерированном файле. По умолчанию `,`",
)
