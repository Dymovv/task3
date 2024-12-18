import csv
import pickle

# Внутреннее представление таблицы: словарь {название_столбца: [значения]}
# Пример: {"Имя": ["Иван", "Анна"], "Возраст": [25, 30]}

# 1. Функции загрузки и сохранения таблиц
def load_table(file_path, file_format="csv"):
    """Загружает таблицу из файла в формате csv или pickle."""
    try:
        if file_format == "csv":
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                table = {column: [] for column in reader.fieldnames}
                for row in reader:
                    for column in table:
                        table[column].append(row[column])
            return table
        elif file_format == "pickle":
            with open(file_path, "rb") as f:
                return pickle.load(f)
        else:
            raise ValueError("Неподдерживаемый формат файла!")
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return None

def save_table(table, file_path, file_format="csv"):
    """Сохраняет таблицу в файл в формате csv, pickle или текстовом виде."""
    try:
        if file_format == "csv":
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                headers = table.keys()
                writer.writerow(headers)
                rows = zip(*table.values())
                writer.writerows(rows)
        elif file_format == "pickle":
            with open(file_path, "wb") as f:
                pickle.dump(table, f)
        elif file_format == "text":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(print_table(table, return_string=True))
        else:
            raise ValueError("Неподдерживаемый формат файла!")
    except Exception as e:
        print(f"Ошибка сохранения файла: {e}")

# 2. Операции с таблицей
def get_rows_by_number(table, start, stop=None, copy_table=False):
    """Получает строки по номерам."""
    rows = {key: values[start:stop] for key, values in table.items()}
    return rows.copy() if copy_table else rows

def get_rows_by_index(table, *values, copy_table=False):
    """Получает строки по значениям первого столбца."""
    first_column = list(table.keys())[0]
    rows = {key: [] for key in table}
    for i, val in enumerate(table[first_column]):
        if val in values:
            for key in table:
                rows[key].append(table[key][i])
    return rows.copy() if copy_table else rows

def get_column_types(table, by_number=True):
    """Возвращает словарь типов данных для столбцов."""
    types = {}
    for idx, (column, values) in enumerate(table.items()):
        sample_value = next((v for v in values if v is not None), None)
        types[idx if by_number else column] = type(sample_value).__name__
    return types

def set_column_types(table, types_dict, by_number=True):
    """Задает типы данных для столбцов."""
    for key, target_type in types_dict.items():
        column = list(table.keys())[key] if by_number else key
        table[column] = [convert_type(val, target_type) for val in table[column]]

def convert_type(value, target_type):
    """Конвертирует значение в указанный тип."""
    try:
        if target_type == "int":
            return int(value)
        elif target_type == "float":
            return float(value)
        elif target_type == "bool":
            return bool(value)
        elif target_type == "str":
            return str(value)
    except:
        return None

def get_values(table, column=0):
    """Возвращает список значений столбца."""
    column_name = list(table.keys())[column] if isinstance(column, int) else column
    return table[column_name]

def set_values(table, values, column=0):
    """Устанавливает значения в столбце."""
    column_name = list(table.keys())[column] if isinstance(column, int) else column
    table[column_name] = values

def print_table(table, return_string=False):
    """Выводит таблицу в текстовом виде."""
    headers = " | ".join(table.keys())
    rows = [" | ".join(str(table[key][i]) for key in table) for i in range(len(next(iter(table.values()))))]
    result = headers + "\n" + "\n".join(rows)
    if return_string:
        return result
    print(result)

# 3. Обработка исключений включена в функции
