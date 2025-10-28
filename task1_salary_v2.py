
def total_salary(path: str) -> tuple[int, float]:
    """
    Читає файл з рядками у форматі "Імʼя,зарплата" і повертає загальну та середню зарплату.
    - Ігнорує порожні рядки та " ".        
    - Рядки з некоректним форматом (не 2 частини, нечислова зарплата, відʼємна зарплата) вважаються критичними помилками.
        Функція збирає всі такі помилки і в кінці викидає ValueError з детальним звітом.    
    - Рядки з зарплатою 0 викликають Warnings, але не вважаються критичними помилками.
    """
    total = 0
    count_valid = 0
    critical_errors = []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line_no, raw_line in enumerate(file, start=1):
                line = raw_line.rstrip('\n')
                parts = [p.strip() for p in line.split(',')]

                # Ігноруємо порожні рядки
                if not line or line.isspace():
                    continue

                # Перевірки формату рядка
                if len(parts) != 2:
                    critical_errors.append(
                        f"[рядок {line_no}] Некоректний формат (очікувався 'Імʼя,зарплата'): «{line}»"
                    )
                    continue

                name, salary_str = parts
                try:
                    salary = int(salary_str)
                except ValueError: # Не int      
                    critical_errors.append(
                        f"[рядок {line_no}] Зарплата не є числом ('{salary_str}'): «{line}»"
                    )
                    continue

                if salary < 0: # Відʼємна зарплата
                    critical_errors.append(
                        f"[рядок {line_no}] Зарплата не може бути відʼємною ({salary}): «{line}»"
                    )
                    continue

                if salary == 0: # Зарплата 0 - Warning але не критична помилка
                    warnings.warn(
                        f"[рядок {line_no}] Зарплата дорівнює 0: «{line}»",
                        UserWarning
                    )
                # якщо всі перевірки пройшли, додаємо до суми і лічильника
                total += salary
                count_valid += 1

    except FileNotFoundError:
        raise ValueError(f"Файл '{path}' не знайдено.")


    if critical_errors:
        raise ValueError("Знайдено критичні помилки (обчислення скасовано):\n" + "\n".join(critical_errors))

    average = total / count_valid if count_valid else 0.0
    return total, average

import warnings

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")  # перехоплюємо всі попередження
    try:
        total, average = total_salary("salary_file.txt")
        print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
    except ValueError as e:
        print(f"Критична помилка: {e}")

if caught:
    print("\nПопередження:")
    for w in caught:
        print(" -", str(w.message))