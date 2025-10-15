from pathlib import Path
import sys
from colorama import Fore, Style, init

init(autoreset=True)  # активируем цветовой вывод

def print_directory(path: Path, indent: int = 0):
    """ 
    Рекурсивно друкує вміст директорії з кольоровим форматуванням.
    - Синій колір для директорій.
    - Зелений колір для файлів.
    - Красний колір для повідомлень про помилки.

    - Відступи та "/" для візуалізації структури.

    - Элементи виводяться в алфавітному порядку.
    
    - Якщо шлях не існує, виводить повідомлення про помилку.
    - Якщо директорія порожня, нічого не друкує.
     """
    
    # Перевірка чи існує шлях на випадок змінення під час виконання рекурсії
    if not path.exists():
        print(Fore.RED + f"Шлях не існує: {path}")
        return

    ITALIC = '\x1b[3m'
    RESET_ITALIC = '\x1b[23m'
    # Якщо це перший запуск, друкуємо назву поточної директорії без відступів та курсивом
    if indent == 0:
        print(ITALIC + Fore.BLUE + Style.BRIGHT + path.name + "/" + Style.RESET_ALL + RESET_ITALIC)

    # Сортируемо, та ітеруємося по елементах директорії
    for item in sorted(path.iterdir()):
        prefix = "  " * (indent + 1)  # відступи

        if item.is_dir():
            # Якщо директорія: друкуємо синім кольором і додаємо "/"
            print(prefix + Fore.BLUE + Style.BRIGHT + item.name + "/" + Style.RESET_ALL)
            print_directory(item, indent + 1)  # викликаемо сами себе для піддиректорії
        else:
            # Якщо файл: друкуємо зеленим кольором
            print(prefix + Fore.LIGHTGREEN_EX + item.name + Style.RESET_ALL)


def main():
    # Перевірка кількості аргументів командного рядка
    if len(sys.argv) < 2:
        print("Використання: python hw03_simple.py <шлях_до_директорії>")
        return

    # Створюємо об'єкт Path з лругого аргумента та перевіряємо чи це директорія
    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(Fore.RED + f"'{directory}' не є директорією.")
        return
    
    # Друкуємо вміст директорії рекурсивно
    print_directory(directory)

#  Якщо файл запущено напряму, а не імпортовано як модуль, то виконуємо main()
if __name__ == "__main__":
    main()
