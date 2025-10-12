def get_cats_info(path:str) -> dict[str, int]:
    cats = [] # type: ignore 
    try:
        with open(path, 'r', encoding='utf-8') as file: # Відкриваємо файл
            for line in file:
                parts = line.strip().split(",") # Розділення рядка на частини
                if len(parts) == 3  : # Перевірка на коректну кількість частин
                    id = parts[0].strip() # ID кота 
                    name = parts[1].strip() # Імʼя кота
                    
                    try:
                        age = int(parts[2].strip()) # Конвертація віку в ціле число
                        if not 0 < age < 40: # Перевірка віку, виключення ValueError
                            raise ValueError(f"Вік повинен бути >0: {age} у рядку:' {line.strip()}'")

                    except ValueError: # Обробка некоректних значень
                        raise ValueError(f"Некоректне значення віку: '{parts[1]}' у рядку:' {line.strip()}'")
                    cats.append({
                        "id": id,
                        "name": name,
                        "age": age,
                        })
                else: # Обробка рядків з некоректною кількістю частин. Виведення попередження, але не виключення
                    print(f"Увага, некоректний формат рядка: '{line.strip()}'")
                    continue

    except FileNotFoundError: # Обробка відсутності файлу
        raise FileNotFoundError(f"Файл '{path}' не знайдено.")
    
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