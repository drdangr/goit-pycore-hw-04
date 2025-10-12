def get_cats_info(path:str) -> list[dict[str, str]]:
    """
    Читає файл з рядками у форматі "ID,Імʼя,Вік" і повертає список словників з інформацією про котів.
    - Рядки з некоректним форматом (не 3 частини, нечисловий вік, відʼємний або нереальний вік) вважаються критичними помилками.
        Функція збирає всі такі помилки і в кінці викидає ValueError з детальним звітом.    
    """
    cats: list[dict[str, str]] = [] 
    errors = []
    count = 0
    try:
        with open(path, 'r', encoding='utf-8') as file: # Відкриваємо файл
            for line in file:
                count += 1
                parts = line.strip().split(",") # Розділення рядка на частини
                if len(parts) == 3  : # Перевірка на коректну кількість частин
                    cat_id = parts[0].strip() # ID кота 
                    name = parts[1].strip() # Імʼя кота
                    # Перевірка і конвертація віку кота
                    try:
                        age = int(parts[2].strip()) # Конвертація віку в ціле число
                        if not 0 < age < 40: # Перевірка віку котів, та котів-довгожителів =), виключення ValueError
                            errors.append(
                                f"Вік повинен бути >0 і <40: {age} у рядку '{count}': '{line.strip()}'"
                            )
                    except ValueError: # Обробка некоректних значень
                        errors.append(
                            f"Некоректне значення віку: '{parts[2]}' у рядку '{count}': '{line.strip()}'"
                        )
                    else:
                        cats.append({
                        "id": cat_id,
                        "name": name,
                        "age": str(age),
                        })
                else: # Обробка рядків з некоректною кількістю частин. 
                    errors.append(
                        f"Некоректний формат рядка (очікувався 'ID,Імʼя,Вік')' у рядку '{count}': '{line.strip()}'"
                    )


    except FileNotFoundError: # Обробка відсутності файлу
        raise FileNotFoundError(f"Файл '{path}' не знайдено.")
    if errors:
        raise ValueError("\n" + "\n".join(errors))
    
    return cats

# Приклад використання функції
try:
    cats_info = get_cats_info("cats_file.txt")
    if cats_info:
        print("Інформація про котів:", cats_info)
    else:
        print("Помилка: Немає валідних рядків у файлі.")
# Обробка виключень
except ValueError as ve:
    print(f"Помилка в данних: {ve}")
except FileNotFoundError as fe:
    print(f"Помилка з файлом: {fe}")