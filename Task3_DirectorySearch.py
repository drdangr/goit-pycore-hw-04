#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Візуалізація структури директорії з кольорами.
Вимоги: Python 3.8+, бібліотека colorama.

Запуск:
    python hw03.py /шлях/до/вашої/директорії
"""

#from __future__ import annotations
import sys
from pathlib import Path
from typing import Iterable
from colorama import init as colorama_init, Fore, Style

# Инициализация colorama (на Windows преобразует ANSI-коды)
colorama_init(autoreset=True)


def print_error(msg: str) -> None:
    """Печать сообщения об ошибке в stderr с красным цветом."""
    sys.stderr.write(Fore.RED + Style.BRIGHT + "Помилка: " + Style.RESET_ALL + msg + "\n")


def list_children_safe(dir_path: Path) -> Iterable[Path]:
    """
    Безопасно получить список дочерних элементов.
    Обрабатывает PermissionError; остальные исключения пробрасывает.
    """
    try:
        return list(dir_path.iterdir())
    except PermissionError:
        # Возвращаем пустой список, а пометку выведем в дереве
        return ()
    except OSError as e:
        # Неожиданная ошибка чтения директории — покажем её и продолжим
        print_error(f"не вдалося прочитати '{dir_path}': {e}")
        return ()


def color_name(p: Path) -> str:
    """Вернуть раскрашенное имя узла в зависимости от типа."""
    name = p.name or str(p)  # на случай корня
    if p.is_symlink():
        return Fore.CYAN + name + Style.RESET_ALL  # симлинки — бирюзовые
    if p.is_dir():
        return Style.BRIGHT + Fore.BLUE + name + "/" + Style.RESET_ALL  # директории — синие, жирные
    return Fore.WHITE + name + Style.RESET_ALL  # файлы — белые


def tree(dir_path: Path, prefix: str = "", is_last: bool = True, mark_perm_issue: bool = False) -> None:
    """
    Рекурсивно печатаем дерево.
    prefix — текущий отступ с "ветками".
    is_last — узел является последним в своём списке братьев.
    mark_perm_issue — отметить у узла, что доступ ограничен.
    """
    connector = "└─ " if is_last else "├─ "
    head = "" if prefix == "" else connector
    suffix = Fore.RED + "  [доступ заборонено]" + Style.RESET_ALL if mark_perm_issue else ""
    # Печать самого узла (для корня `prefix == ""` печатаем без коннектора)
    if prefix == "":
        print(color_name(dir_path))
    else:
        print(prefix + head + color_name(dir_path) + suffix)

    # Если не директория — рекурсия не нужна
    if not dir_path.is_dir():
        return

    # Составим новый префикс для потомков
    child_prefix = prefix + ("   " if is_last else "│  ")

    # Получаем дочерние
    children = list_children_safe(dir_path)
    perm_issue = False
    try:
        # Сортируем: сначала директории, потом файлы; далее по имени (кейсы игнорируем)
        children_sorted = sorted(
            children,
            key=lambda p: (not p.is_dir(), p.name.lower())
        )
        # Если пусто — просто выходим
        if not children_sorted:
            return
    except Exception as e:
        print_error(f"не вдалося обробити вміст '{dir_path}': {e}")
        return

    # Если список был пуст из-за PermissionError — children == ()
    if children == ():
        # пометим узел (уже напечатан), и выходим
        # (пометка уже отображена через suffix, если мы бы её передали — однако
        # мы определим это чуть иначе: если пусто и реально есть дочерние? Мы не знаем.
        # Сделаем дополнительный дубль с пометкой у детей не печатаем.)
        return

    # Обходим потомков
    for idx, child in enumerate(children_sorted):
        last = (idx == len(children_sorted) - 1)

        # Узнаем, сможем ли прочитать дочерние для каталога `child`
        mark_child_perm = False
        if child.is_dir():
            try:
                _ = list(child.iterdir())
            except PermissionError:
                mark_child_perm = True
            except OSError:
                pass

        tree(child, prefix=child_prefix, is_last=last, mark_perm_issue=mark_child_perm)


def main(argv: list[str]) -> int:
    # Требование: использовать sys для получения аргумента командной строки
    if len(argv) < 2:
        print_error("не вказано шлях до директорії.\nПриклад: python hw03.py /шлях/до/вашої/директорії")
        return 2

    raw_path = argv[1]
    p = Path(raw_path).expanduser().resolve()

    # Валидация пути
    if not p.exists():
        print_error(f"шлях не існує: {p}")
        return 1
    if not p.is_dir():
        print_error(f"це не директорія: {p}")
        return 1

    # Печатаем дерево
    try:
        tree(p)
    except KeyboardInterrupt:
        print_error("перервано користувачем (Ctrl+C)")
        return 130
    except Exception as e:
        print_error(f"неочікувана помилка: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
