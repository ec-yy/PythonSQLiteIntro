import re

# Functions for checking right table and record pre-existence.
def right_table(table):
    right_tables = {"Airport", "Route", "Pilot", "Flight"}
    if not table in right_tables:
        print(f"{table} is not valid.")
        return False
    return True


def record_exists(cursor, table, primary_key_column, primary_key_value):  
    if not right_table(table):
        return False
    
    query = f"SELECT 1 FROM {table} WHERE {primary_key_column} = ?"
    cursor.execute(query, (primary_key_value,))
    return cursor.fetchone() is not None


# Functions for user input validation.
def non_empty_input(system_prompt):
    while True:
        user_input = input(system_prompt).strip()
        if user_input:
            return user_input
        print("User input must be non-empty. Try again.")


def integer_input(system_prompt):
    while True:
        user_input = input(system_prompt).strip()
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input. User input must be an integer. Try again.")


def positive_integer_input(system_prompt):
    while True:
        user_input = input(system_prompt).strip()
        try:
            value = int(user_input)
            if value > 0:
                return value
            else:
                print("Invalid input. User input must be a positive integer. Try again.")
        except ValueError:
            print("Invalid input. User input must be an integer. Try again.")


def boolean_input(system_prompt):
    while True:
        user_input = input(system_prompt).strip().upper()
        if user_input in ("Y", "N"):
            return user_input
        else:
            print("Invalid input. User input must be Y or N only. Try again.")


def conformed_id_input(system_prompt, pattern, example):
    while True:
        user_input = input(system_prompt).strip().upper()

        if not user_input:
            print("User input must be non-empty. Try again.")
            continue

        if re.fullmatch(pattern, user_input):
            return user_input
        else:
            print(f"Invalid input. The input should conform to a prescribed format (e.g., {example}). Try again.")


# General function for view of complete records of a table.
def view_table(cursor, table_name, columns="*", order_by=None):
    query = f"SELECT {columns} FROM {table_name}"
    if order_by:
        query = query + f" ORDER BY {order_by}"

    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print(f"No records were found in {table_name}.")
        return

    print(f"\n<--- {table_name} Complete Records --->")
    for row in rows:
        print(row)
