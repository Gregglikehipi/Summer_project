import sqlite3

class DBHelper:

    def __init__(self, db_name = "recipe.db"):
        self.dbname = f"sqlite3:/{db_name}"
        self.conn = sqlite3.connect(db_name)

    #for link, recipe, ingredient and category
    def create_table_simple(self, table_name, params):
        column = ""
        for i in range(len(params) - 1):
            column += params[i] + " TEXT, "
        column += params[len(params) - 1] + " TEXT "

        new_table = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT , {column})"
        #print(new_table)
        try:
            #print(new_table)
            self.conn.execute(new_table)
            self.conn.commit()
        except sqlite3.Error as err:
            #print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()

    #for calories and recipe_ingredients
    def create_table(self, table_name, primary_key, foreign_table_name, foreign_col, another_foreign_col, params, auto = False):
        column = ""
        for i in range(len(params) - 1):
            column += params[i] + " TEXT, "
        column += params[len(params)-1] + " TEXT "

        foreign_key = f"FOREIGN KEY ({foreign_col})  REFERENCES {foreign_table_name} ({another_foreign_col})"

        new_table = f"CREATE TABLE IF NOT EXISTS {table_name} ({primary_key} INTEGER PRIMARY KEY {('', 'AUTOINCREMENT')[auto == True]} , {column}, {foreign_key})"

        try:
            #print(new_table)
            self.conn.execute(new_table)
            self.conn.commit()
        except sqlite3.Error as err:
            #print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()

    #id autoincrement
    def generic_create_table(self, table_name, primary_keys, foreign_keys, references, unique_args, other_args, auto):

        new_table = ""

        begin = f"CREATE TABLE IF NOT EXISTS {table_name} ("

        primary = ""
        column = " "

        if len(primary_keys) > 1:
            for i in range(len(primary_keys) - 1):
                primary += primary_keys[i][0] + ", "
                column += primary_keys[i][0] + f" {primary_keys[i][1]}, "

            primary += primary_keys[len(primary_keys) - 1][0]
            column += primary_keys[len(primary_keys) - 1][0] + f" {primary_keys[len(primary_keys) - 1][1]}, "

            new_table += f"PRIMARY KEY ({primary})"
        else:
            begin += f"{primary_keys[0][0]} {primary_keys[0][1]} PRIMARY KEY {('', 'AUTOINCREMENT')[auto]}"
            column += ", " + column

        if foreign_keys is not None and len(foreign_keys) != 0:
            reference = ""
            for i in range(len(references) - 1):
                reference += f"FOREIGN KEY ({foreign_keys[i]}) REFERENCES {references[i][0]}({references[i][1]}), "
                column += foreign_keys[i] + " TEXT, "
            reference += f"FOREIGN KEY ({foreign_keys[len(foreign_keys) - 1]}) REFERENCES" \
                         f" {references[len(references) - 1][0]}({references[len(references) - 1][1]})"
            column += foreign_keys[len(foreign_keys) - 1] + " TEXT, "

            new_table += f", {reference}"

        if unique_args is not None and len(unique_args) != 0:
            unique = ""
            for i in range(len(unique_args) - 1):
                unique += unique_args[i] + ", "
                column += unique_args[i] + " TEXT, "
            unique += unique_args[len(unique_args) - 1]
            column += unique_args[len(unique_args) - 1] + " TEXT, "

            new_table += f", UNIQUE ({unique})"

        if other_args is not None and len(other_args) != 0:
            for i in range(len(other_args) - 1):
                column += other_args[i] + " TEXT, "
            column += other_args[len(other_args)-1] + " TEXT, "

        new_table = begin + (column, column[:-2])[len(primary_keys) == 1] + new_table + ")"

        try:
            #print(new_table)
            self.conn.execute(new_table)
            #print("Выполнилось")
            self.conn.commit()
        except sqlite3.Error as err:
            #print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()


    def get_unique(self, table_name, name, unique_columns):
        column = ""
        for i in range(len(unique_columns) - 1):
            column += unique_columns[i] + ", "
        column += unique_columns[len(unique_columns)-1]

        try:
            #print("Unique")
            self.conn.execute(f"CREATE UNIQUE INDEX {name} ON {table_name}({column})")
            #print("Выполнилось")
            self.conn.commit()
        except sqlite3.Error as err:
            #print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()

    def update(self, table_name, column_arg, arg, column_change, change):
        update = f"UPDATE {table_name} " \
                 f"SET {column_change} = '{change}' " \
                f"WHERE {column_arg} = '{arg}' "
        try:
            print(update)
            self.conn.execute(update)
            print("Выполнилось")
            self.conn.commit()
        except sqlite3.Error as err:
            print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()

    def delete(self, table_name, column_arg, arg):
        update = f"DELETE FROM {table_name} " \
                 f"WHERE {column_arg} = '{arg}' "
        try:
            # print(new_insert)
            self.conn.execute(update)
            # print("Выполнилось")
            self.conn.commit()
        except sqlite3.Error as err:
            # print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()

    def insert_check(self, table_name, primary_key, primary_value, args):
        arguments = f"'{primary_value}', '"
        for i in range(len(args) - 1):
            arguments += str(args[i]) + "', '"
        arguments += str(args[len(args) - 1]) + "'"
        #print(arguments)

        new_insert = f"INSERT INTO {table_name} SELECT * FROM (SELECT {arguments}) AS tmp " \
                     f"WHERE NOT EXISTS ( SELECT {primary_key} FROM {table_name} WHERE {primary_key} = '{primary_value}'" \
                     f") LIMIT 1"
        try:
            #print(new_insert)
            self.conn.execute(new_insert)
            #print("Выполнилось")
            self.conn.commit()
        except sqlite3.Error as err:
            #print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()

    def insert(self, table_name, column_args, args):
        arguments = "'"
        for i in range(len(args) - 1):
            arguments += str(args[i]) + "', '"
        arguments += str(args[len(args) - 1]) + "'"
        #print(arguments)

        columns = ""
        for i in range(len(column_args) - 1):
            columns += str(column_args[i]) + ", "
        columns += str(column_args[len(column_args) - 1])

        new_insert = f"INSERT INTO {table_name} ({columns}) VALUES ({arguments})"
        #print(new_insert)

        try:
            print(new_insert)
            self.conn.execute(new_insert)
            #print("Выполнилось")
            self.conn.commit()
            return True
        except sqlite3.Error as err:
            print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()
            return False

    def print_info(self, table_name):
        new_get = f"SELECT * FROM {table_name}"
        cursor = self.conn.execute(new_get)

        #print("Выполнилось")

        return [row for row in cursor]

    def get(self, table_name, column_args, args):
        query = ""
        for i in range(len(column_args) - 1):
            query += column_args[i] + " = '" + args[i] + "' AND "
        query += column_args[len(column_args) - 1] + " = '" + args[len(column_args) - 1] + "'"

        new_get = f"SELECT * FROM {table_name} WHERE {query}"
        #print(new_get)

        cursor = self.conn.execute(new_get)

        return [row for row in cursor]

    def rollback(self):
        self.conn.rollback()

    #def update(self, flat_id, updates):


    #def delete(self, flat_id):