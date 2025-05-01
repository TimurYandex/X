import datetime
import json
from pprint import pprint

n_h_w = '''пн,6,3
вт,6,4
ср,6,5
чт,6,6
пт,7,4
сб,7,5
вс,7,6
янв,0,0
фев,0,1
мар,0,2
апр,0,3
май,0,4
июн,0,5
июл,1,0
авг,1,1
сен,1,2
окт,1,3
ноя,1,4
дек,1,5
1,2,0
2,2,1
3,2,2
4,2,3
5,2,4
6,2,5
7,2,6
8,3,0
9,3,1
10,3,2
11,3,3
12,3,4
13,3,5
14,3,6
15,4,0
16,4,1
17,4,2
18,4,3
19,4,4
20,4,5
21,4,6
22,5,0
23,5,1
24,5,2
25,5,3
26,5,4
27,5,5
28,5,6
29,6,0
30,6,1
31,6,2'''


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


save_dict_json('calendar_home', n_h_w_dict)

calendar_cells = read_dict_json('calendar_home')
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

f1 = Figure(['L', (0, 0), (0, 1), (0, 2), (0, 3), (1, 3)])
f2 = Figure(['N', (0, 0), (0, 1), (0, 2), (1, 2), (1, 3)])
f3 = Figure(['s', (0, 0), (0, 1), (1, 1), (1, 2)])
f4 = Figure(['l', (0, 0), (0, 1), (0, 2), (1, 2)])
f5 = Figure(['V', (0, 0), (0, 1), (0, 2), (1, 0),(2, 0)])
f6 = Figure(['I', (0, 0), (0, 1), (0, 2), (0, 3)])
f7 = Figure(['P', (0, 0), (0, 1), (0, 2), (1, 1),(1, 2)])
f8 = Figure(['T', (0, 0), (0, 1), (0, 2), (1, 1),(2, 1)])
f9 = Figure(['Z', (0, 0), (0, 1), (1, 1), (2, 1),(2, 2)])
f0 = Figure(['C', (0, 0), (0, 1), (1, 0), (0, 2),(1, 2)])


figures = [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9]
pprint(figures)
# и для каждой фигуры получаем ее варианты и добавляем в общий словарь вариантов
f_vars = {}
for fig in figures:
    for variant in fig.variants:
        f_vars[variant] = fig.variants[variant]

# Создаем доску некоторой формы, вырезая ненужные клетки из прямоугольника
b = Board(8, 7)
# вырез снизу слева
for i in range(4):
    b.flip(7, i)
# вырез справа вверху
for i in range(2):
    b.flip(i, 6)
date_string = '2025-05-02'
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
create_colored_excel(unique_solutions, "calendar_home.xlsx")

dlx = DLX(matrix, column_names)
all_solutions = dlx.solve_iteratively()
unique_solutions = find_unique_matrices([solution2matrix(m) for m in show(all_solutions)])
create_colored_excel(unique_solutions, "calendar_home_unique.xlsx")
