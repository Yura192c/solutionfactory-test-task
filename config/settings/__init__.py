import os
import sys

# Получить путь к текущему скрипту
current_dir = os.path.dirname(os.path.abspath(__file__))

# Построить путь к файлу .env на 3 уровня выше текущего скрипта
env_file_path = os.path.abspath(os.path.join(current_dir, '../../.env'))

# Проверить, существует ли файл .env
if os.path.exists(env_file_path):
    # Открыть файл .env и считать его содержимое
    with open(env_file_path) as file:
        env_vars = file.readlines()

    # Проход по каждой строке файла
    for line in env_vars:
        # Пропустить пустые строки
        if not line.strip() or line.strip().startswith('#'):
            continue

        # Разделить строку на имя переменной и значение
        key, value = line.strip().split('=')
        # Установить переменную окружения
        os.environ[key] = value
else:
    print(f"Файл .env не найден по пути: {env_file_path}")
    sys.exit(1)