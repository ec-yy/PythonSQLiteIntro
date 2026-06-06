import re
from datetime import datetime

# ── Functions for checking right table and record pre-existence ────────────────────────────────────────────────────────────
def valid_table(table):
    valid_tables = {"Airport", "Route", "Pilot", "Flight"}
    if not table in valid_tables:
        print(f"{table} is not valid.")
        return False
    return True


def record_exists(cursor, table, primary_key_column, primary_key_value):  
    if not valid_table(table):
        return False
    
    query = f"SELECT 1 FROM {table} WHERE {primary_key_column} = ?"
    cursor.execute(query, (primary_key_value,))
    return cursor.fetchone() is not None


# ── Functions for user input validation ────────────────────────────────────────────────────────────
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





def valid_choice(system_prompt, choice):
    hint = " / ".join(choice)
    while True:
        user_input = input(system_prompt).strip().upper()
        if user_input in choice:
            return user_input
        print(f"Sorry. Invalid input. User input must be from {hint} only. Try again.")


def valid_id_input(system_prompt, pattern, example):
    while True:
        user_input = input(system_prompt).strip().upper()

        if not user_input:
            print("User input must be non-empty. Try again.")
            continue

        if re.fullmatch(pattern, user_input):
            return user_input
        else:
            print(f"Invalid input. The input should conform to a prescribed format (e.g., {example}). Try again.")


def valid_date_time_format(system_prompt, mandatory_input)
    """
    Repeatedly prompts the user until a valid datetime is entered
    in YYYY-MM-DD HH:MM:SS format.

    - Uses datetime.strptime to validate both format AND calendar logic
      (e.g. rejects Feb 31, month 13, hour 25, etc.)
    - Re-formats via strftime to normalise edge cases
      (e.g. user types 2026-6-6 9:5:0 → stored as 2026-06-06 09:05:00)
    - Returns the validated string, ready for SQLite datetime() calculations.
    """
    pattern = "%Y-%m-%d %H:%M:%S"
    while True:
        if mandatory_input == True:
            user_input = non_empty_input(system_prompt)
        else:
            user_input = input(system_prompt).strip()
            if not user_input:
                return None
        try:
            parsed_input = datetime.strptime(user_input, pattern)
            return parsed_input.strftime(pattern)
        except ValueError:
            print("Sorry. The date and time format is invalid. Please use YYYY-MM-DD HH:MM:SS (e.g. 2026-06-06 14:30:00). Try again.")


def valid_date_format(system_prompt):
    """
    Prompts the user for a date in YYYY-MM-DD format.
    - Allows blank input (returns None) — used for optional search filters.
    - Uses datetime.strptime to validate calendar logic
      (e.g. rejects Feb 31, month 13, etc.)
    - Returns the validated date string, or None if left blank.
    """
    pattern = "%Y-%m-%d"
    while True:
        user_input = non_empty_input(system_prompt)
        try:
            parsed_input = datetime.strptime(user_input, pattern)
            return parsed_input.strftime(pattern)
        except ValueError:
            print("Sorry. The date format is invalid. Please use YYYY-MM-DD (e.g. 2026-06-06). Try again.")

# ── General function for view of complete records of a table ────────────────────────────────────────────────────────────
def view_table(cursor, table_name, columns="*", order_by=None):
    query = f"SELECT {columns} FROM {table_name}"
    if order_by:
        query = query + f" ORDER BY {order_by}"

    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print(f"No records were found in {table_name}.")
        return

    print(f"\n<----- {table_name} Complete Records ----->")
    for row in rows:
        print(row)
