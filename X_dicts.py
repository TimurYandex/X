from pprint import pprint
from typing import Dict, List, Set, Generator, Any


def solve(cols: Dict[str, Set[str]], rows: Dict[str, List[str]], solution=None, k=0) -> Generator[
    List[str], None, None]:
    k += 1
    if solution is None:
        solution = []
    if not cols:
        # Если все столбцы покрыты, возвращаем текущее решение
        yield list(solution)
        return
    # Эвристика выбора столбца: выбираем столбец с минимальным количеством строк
    c = min(cols, key=lambda z: len(cols[z]))
    for r in list(cols[c]):
        # Добавляем строку в текущее решение
        solution.append(r)
        # Удаляем все столбцы, которые покрываются выбранной строкой
        removed_cols = select(cols, rows, r)
        # Рекурсивно ищем решение для оставшихся столбцов
        yield from solve(cols, rows, solution,k)
        # Восстанавливаем удаленные строки и столбцы
        deselect(cols, rows, r, removed_cols)
        # Убираем строку из текущего решения
        solution.pop()


def select(x: Dict[str, Set[str]], y: Dict[str, List[str]], r: str) -> List[Set[str]]:
    # запоминаем удаляемые столбцы для последующего восстановления
    cols = []
    # в выбранной строке выбираем по очереди все столбцы
    for j in y[r]:
        # Удаляем все строки в этом столбце
        for i in x[j]:
            for k in y[i]:
                if k != j:
                    x[k].remove(i)
        # Удаляем столбец и сохраняем его для последующего восстановления
        cols.append(x.pop(j))
    return cols


def deselect(x: Dict[str, Set[str]], y: Dict[str, List[str]], r: str, cols: List[Set[str]]) -> None:
    for j in reversed(y[r]):
        # Восстанавливаем столбец
        x[j] = cols.pop()
        # Восстанавливаем строки в этом столбце
        for i in x[j]:
            for k in y[i]:
                if k != j:
                    x[k].add(i)


def encode(matrix: List[List[int]], column_names: List[str]) -> tuple[Dict[str, Set[str]], Dict[str, List[str]]]:
    # Инициализация словарей для хранения столбцов и строк
    cols = {name: set() for name in column_names}
    rows = {}
    for row in matrix:
        # Преобразуем строку в уникальный идентификатор
        i = "".join(map(str, row))
        rows[i] = []
        for j, name in enumerate(column_names):
            if row[j]:
                # Добавляем строку в столбец
                rows[i].append(name)
                cols[name].add(i)
    return cols, rows

def show(x, y, s):
    print("\nСтолбцы:")
    pprint(x)
    print("\nСтроки:")
    pprint(y)
    print("\nРешения (решением является список заголовков выбранных строк покрытий):")
    pprint(s)
    try:
        print([y[r] for r in s])
    except:
        print(s, "не получилось")


# Пример использования:
if __name__ == "__main__":
    matrix = [
        [1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 1],
        [0, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 1],
    ]
    column_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    X, Y = encode(matrix, column_names)
    s = solve(X, Y)
    print(next(s))
    print(next(s))
    print(next(s))
    print(next(s))
    print(next(s))
    print(next(s))



    # pprint(s)
    # print()
    # for t in s:
    #     pprint([Y[i] for i in t])
    #

