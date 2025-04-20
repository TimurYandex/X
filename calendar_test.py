import datetime
import json
from pprint import pprint

n_h_w = '''пн,1,1
вт,0,1
ср,0,2
чт,1,0
пт,0,0
сб,1,2
вс,2,0
21,3,1
апр,3,2'''



def create_dict_from_str(cal):
    data_dict = {}
    for line in cal.split():
        row = line.split(',')
        if len(row) == 3:
            key = row[0]
            try:
                value = (int(row[1]), int(row[2]))
                data_dict[key] = value
            except ValueError:
                print(f"Warning: Could not convert values to integers in row: {row}")
        else:
            print(f"Warning: Skipping row with incorrect number of elements: {row}")
    return data_dict


n_h_w_dict = create_dict_from_str(n_h_w)


def read_dict_json(filename: str):
    with open(filename + ('.json' if filename[-5:] != '.json' else ''), encoding='UTF8') as f:
        cal = {a: tuple(b) for a, b in json.loads(f.read()).items()}
    return cal


def save_dict_json(filename: str, calendar_cells: dict):
    with open(filename + ('.json' if filename[-5:] != '.json' else ''), 'w', encoding='UTF8') as f:
        f.write(json.dumps(calendar_cells, ensure_ascii=False, indent=4))


save_dict_json('calendar_test', n_h_w_dict)

calendar_cells = read_dict_json('calendar_test')
pprint(calendar_cells)


def format_date_ru(date_str):
    """
    Formats a date string into a tuple of (weekday, day, month) in Russian.

    Args:
        date_str (str): A date string in the format 'YYYY-MM-DD'.

    Returns:
        tuple: A tuple containing the weekday (short format in Russian),
               day (string), and month (short format in Russian).
               Returns None if the input date is invalid.
    """

    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        weekday = date_obj.strftime('%w')  # 0 is Sunday, 1 is Monday, ..., 6 is Saturday
        weekday_names = ['вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб']
        weekday_ru = weekday_names[int(weekday)]
        day = str(date_obj.day)
        month = date_obj.strftime('%m')
        month_names = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
        month_ru = month_names[int(month) - 1]

        return weekday_ru, day, month_ru
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return None


# Задаем фигуры для покрытия
from dancing import DLX, show
from xl import *
from board import Figure, generate_column_names, Board, generate_matrix

f0 = Figure(['L', (0, 0), (0, 1), (1, 1)])
f1 = Figure(['I', (0, 0), (0, 1), (0, 2)])
f2 = Figure(['i', (0, 0), (0, 1)])

figures = [f0, f1, f2]
pprint(figures)
# и для каждой фигуры получаем ее варианты и добавляем в общий словарь вариантов
f_vars = {}
for fig in figures:
    for variant in fig.variants:
        f_vars[variant] = fig.variants[variant]

# Создаем доску некоторой формы, вырезая ненужные клетки из прямоугольника
b = Board(3, 3)
# # вырез снизу слева
# for i in range(4):
#     b.flip(7, i)
# # вырез справа вверху
# for i in range(2):
#     b.flip(i, 6)
date_string = '2025-04-21'
formatted_date = format_date_ru(date_string)
for cell in formatted_date:
    b.flip(calendar_cells[cell])
print(b)
# Список заголовков столбцов, где часть - клетки поля, а часть - уникальные типы фигурок
column_names = generate_column_names(b, f_vars)
print(column_names)
# создаем матрицу всех строк, соответствующих уникальным расположениям фигурок на поле
matrix = generate_matrix(b, f_vars, column_names)

dlx = DLX(matrix, column_names)
all_solutions = dlx.solve()
unique_solutions = find_unique_matrices([solution2matrix(m) for m in show(all_solutions)])
create_colored_excel(unique_solutions, "calendar_test.xlsx")

dlx = DLX(matrix, column_names)
all_solutions = dlx.solve_iteratively()
unique_solutions = find_unique_matrices([solution2matrix(m) for m in show(all_solutions)])
create_colored_excel(unique_solutions, "calendar_test_unique.xlsx")
