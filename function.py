def checking_empty_input(system_prompt):
    while True:
        user_input = input(system_prompt).strip()
        if user_input:
            return user_input
        print("User input must not be empty. Try again.")

def view_table(cursor, table_name, columns="*", order_by=None):
    allowed_tables = {"Airport", "Route", "Pilot", "Flight"}
    if table_name not in allowed_tables:
        print("Invalid table name.")
        return

    query = f"SELECT {columns} FROM {table_name}"
    if order_by:
        query += f" ORDER BY {order_by}"

    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print(f"No records found in {table_name}.")
        return

    print(f"\n=== {table_name} Records ===")
    for row in rows:
        print(row)


def require_integer(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid integer.")

def record_exists(cursor, table, pk_column, pk_value):
    allowed_tables = {"Airport", "Route", "Pilot", "Flight"}
    if table not in allowed_tables:
        return False

    query = f"SELECT 1 FROM {table} WHERE {pk_column} = ?"
    cursor.execute(query, (pk_value,))
    return cursor.fetchone() is not None

