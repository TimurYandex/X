import csv
import datetime
import json
from pprint import pprint

n_h_w = '''пн,0,8
вт,0,9
ср,1,9
чт,2,9
пт,3,9
сб,4,9
вс,4,8
янв,0,0
фев,0,1
мар,0,2
апр,0,3
май,1,0 
июн,1,1 
июл,3,0
авг,3,1
сен,4,0
окт,4,1
ноя,4,2
дек,4,3
1,0,4
2,0,5
3,0,6
4,0,7
5,1,2
6,1,3
7,1,4
8,1,5
9,1,6
10,1,7
11,1,8
12,2,0
13,2,1
14,2,2
15,2,3
16,2,4
17,2,5
18,2,6
19,2,7
20,2,8
21,3,2
22,3,3
23,3,4
24,3,5
25,3,6
26,3,7
27,3,8
28,4,4
29,4,5
30,4,6
31,4,7'''



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


def save_dict_json(filename: str, calendar_cells:dict):
    with open(filename + ('.json' if filename[-5:] != '.json' else ''), 'w', encoding='UTF8') as f:
        f.write(json.dumps(calendar_cells, ensure_ascii=False, indent=4))

save_dict_json('calendar_school', n_h_w_dict)

calendar_cells = read_dict_json('calendar_school')


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

        return (weekday_ru, day, month_ru)
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return None


# Задаем фигуры для покрытия
from dancing import DLX, show
from xl import *
from board import Figure, generate_column_names, Board, generate_matrix

f1 = Figure(['L', (0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1)])
f2 = Figure(['P', (0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1)])
f3 = Figure(['F', (0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 2)])
f4 = Figure(['T', (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1)])
f5 = Figure(['H', (0, 0), (0, 1), (1, 1), (2, 0), (2, 1), (2, 2)])
f6 = Figure(['S', (0, 0), (0, 1), (1, 0), (2, 0), (2, 1), (3, 1)])
f7 = Figure(['W', (0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)])
f8 = Figure(['D', (0, 0), (0, 1), (0, 2), (1, 1), (1, 2)])
figures = [f1, f2, f3, f4, f5, f6, f7, f8]
# и для каждой фигуры получаем ее варианты и добавляем в общий словарь вариантов
f_vars = {}
for fig in figures:
    for variant in fig.variants:
        f_vars[variant] = fig.variants[variant]

# Создаем доску некоторой формы, вырезая ненужные клетки из прямоугольника
b = Board(5, 10)
date_string = '2025-05-02'
formatted_date = format_date_ru(date_string)
for cell in formatted_date:
    b.flip(calendar_cells[cell])


# Список заголовков столбцов, где часть - клетки поля, а часть - уникальные типы фигурок
column_names = generate_column_names(b, f_vars)
print(column_names)

# создаем матрицу всех строк, соответствующих уникальным расположениям фигурок на поле
matrix = generate_matrix(b, f_vars, column_names)

dlx = DLX(matrix, column_names)
all_solutions = dlx.solve()
unique_solutions = find_unique_matrices([solution2matrix(m) for m in show(all_solutions)])
create_colored_excel(unique_solutions, "calendar_school.xlsx")

dlx = DLX(matrix, column_names)
all_solutions = dlx.solve_iteratively()
unique_solutions = find_unique_matrices([solution2matrix(m) for m in show(all_solutions)])
create_colored_excel(unique_solutions, "calendar_school_unique.xlsx")
