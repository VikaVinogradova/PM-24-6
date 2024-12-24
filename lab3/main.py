import csv
import pickle
from datetime import datetime


movies_data = [
    ["Побег из Шоушенка", "Триллер", 1994, 9.3],
    ["Форест Гамп", "Романтика", 1994, 8.6],
    ["Крестный отец", "Драма", 1972, 9.1]
]


cartoons_data = [
    ["Король Лев", "Анимация", 1994, 8.5],
    ["Шрек", "Анимация", 2001, 7.9],
    ["Зверополис", "Анимация", 2016, 8.0]
]


class Table:
    def __init__(self, columns):
        self.columns = columns  
        self.data = []  

    def add_row(self, row):
        if len(row) != len(self.columns):
            raise ValueError("Количество значений в строке не соответствует количеству столбцов")
        self.data.append(row)

    def get_rows_by_number(self, start, stop=None, copy_table=False):
        if stop is None:
            stop = start + 1  
        rows = self.data[start:stop]
        if copy_table:
            rows = rows.copy()  
        return rows

    def get_rows_by_index(self, *vals, copy_table=False):
        rows = [row for row in self.data if row[0] in vals]
        if copy_table:
            rows = rows.copy()  
        return rows

    def get_column_types(self, by_number=True):
        types = {}
        for idx, column in enumerate(self.columns):
            column_values = [row[idx] for row in self.data]
            if all(isinstance(val, int) for val in column_values):
                types[column] = int
            elif all(isinstance(val, float) for val in column_values):
                types[column] = float
            else:
                types[column] = str
        return types

    def set_column_types(self, types_dict, by_number=True):
        for col, col_type in types_dict.items():
            col_idx = self.columns.index(col) if not by_number else col
            for row in self.data:
                row[col_idx] = col_type(row[col_idx])

    def get_values(self, column=0):
        if isinstance(column, int):
            return [row[column] for row in self.data]
        else:
            col_idx = self.columns.index(column)
            return [row[col_idx] for row in self.data]

    def get_value(self, column=0):
        if isinstance(column, int):
            return self.data[0][column]
        else:
            col_idx = self.columns.index(column)
            return self.data[0][col_idx]

    def set_values(self, values, column=0):
        if isinstance(column, int):
            for i in range(len(self.data)):
                self.data[i][column] = values[i]
        else:
            col_idx = self.columns.index(column)
            for i in range(len(self.data)):
                self.data[i][col_idx] = values[i]

    def set_value(self, value, column=0):
        if isinstance(column, int):
            self.data[0][column] = value
        else:
            col_idx = self.columns.index(column)
            self.data[0][col_idx] = value

    def print_table(self):
        print(f"{' | '.join(self.columns)}")
        print('-' * 50)
        for row in self.data:
            print(' | '.join(str(val) for val in row))

    # Дополнительные функции

    
   
    def load_table_from_files(self,*files):
        tables = []
        for file in files:
            if file.endswith('.csv'):
                with open(file, mode='r', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    header = next(reader)
                    table = Table(columns=header)
                    for row in reader:
                        table.add_row(row)
                    tables.append(table)
            elif file.endswith('.pkl'):
                with open(file, mode='rb') as pkl_file:
                    table_data = pickle.load(pkl_file)
                    table = Table(columns=table_data[0])
                    for row in table_data[1]:
                        table.add_row(row)
                    tables.append(table)
        return tables

    
    def save_table_to_files(self, max_rows, base_filename, file_format="csv"):
        rows = self.data
        files = []
        for i in range(0, len(rows), max_rows):
            filename = f"{base_filename}_{i // max_rows + 1}.{file_format}"
            files.append(filename)
            if file_format == "csv":
                with open(filename, mode='w', encoding='utf-8', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(self.columns)
                    writer.writerows(rows[i:i + max_rows])
            elif file_format == "pkl":
                with open(filename, mode='wb') as pkl_file:
                    pickle.dump([self.columns, rows[i:i + max_rows]], pkl_file)
        return files

    
    
    def concat(self, table1, table2):
        if table1.columns != table2.columns:
            raise ValueError("Таблицы должны иметь одинаковую структуру")
        table1.data.extend(table2.data)
        return table1

    
    def split(self, row_number):
        table1 = Table(columns=self.columns)
        table2 = Table(columns=self.columns)
        table1.data = self.data[:row_number]
        table2.data = self.data[row_number:]
        return table1, table2

    
    def auto_detect_column_types(self):
        types = {}
        for idx, column in enumerate(self.columns):
            column_values = [row[idx] for row in self.data]
            if all(isinstance(val, int) for val in column_values):
                types[column] = int
            elif all(isinstance(val, float) for val in column_values):
                types[column] = float
            elif all(isinstance(val, str) for val in column_values):
                types[column] = str
            elif all(isinstance(val, datetime) for val in column_values):
                types[column] = datetime
            else:
                types[column] = str
        return types



movies = Table(columns=["Название фильма", "Жанр", "Год выпуска", "Оценка IMDb"])
for row in movies_data:
    movies.add_row(row)

cartoons = Table(columns=["Название мультфильма", "Жанр", "Год выпуска", "Оценка IMDb"])
for row in cartoons_data:
    cartoons.add_row(row)


print("Таблица фильмов:")
movies.print_table()

print("\nТаблица мультфильмов:")
cartoons.print_table()


movies_from_files = Table.load_table_from_files('movies_part1.csv', 'movies_part2.csv')


movies.save_table_to_files(max_rows=2, base_filename="movies_split", file_format="csv")


print("\nОбъединение таблиц:")
concatenated_table = Table.concat(movies, cartoons)
concatenated_table.print_table()


print("\nРазделение таблицы:")
table1, table2 = movies.split(2)
table1.print_table()
table2.print_table()


print("\nАвтоматическое определение типов столбцов:")
print(movies.auto_detect_column_types())
