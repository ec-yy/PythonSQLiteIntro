from rule import conformed_id_input, non_empty_input, boolean_input, record_exists


def add_new_flight(connection, cursor):
    print("\n<----- Add New Flight ----->")

    flight_id = conformed_id_input("Please provide flight ID (e.g., F001): ", r"^[A-Z]{1}[0-9]{3}$", "e.g., F001")
    if record_exists(cursor, "Flight", "flight_id", flight_id):
        print(f"Sorry. Flight {flight_id} already exists.")
        return

    departure = non_empty_input("Departure date and time (YYYY-MM-DD HH:MM:SS): ")

    status_choice = boolean_input("Select status (1 = Scheduled, 2 = Delayed): ", "1/2")
    status = "Scheduled" if status_choice == "1" else "Delayed"

    route_id = conformed_id_input("Route ID (e.g., CX001): ", r"^[A-Z]{2}[0-9]{3}$", "e.g., CX001")
    if not record_exists(cursor, "Route", "route_id", route_id):
        print(f"Sorry. Route {route_id} not found.")
        return

    captain_id = conformed_id_input("Captain pilot ID (e.g., P001): ", r"^[A-Z]{1}[0-9]{3}$", "e.g., P001")
    if not record_exists(cursor, "Pilot", "pilot_id", captain_id):
        print(f"Sorry. Pilot {captain_id} not found.")
        return

    officer_id = conformed_id_input("First Officer pilot ID (e.g., P002): ", r"^[A-Z]{1}[0-9]{3}$", "e.g., P002")
    if not record_exists(cursor, "Pilot", "pilot_id", officer_id):
        print(f"Sorry. Pilot {officer_id} not found.")
        return

    try:
        cursor.execute("""
            INSERT INTO Flight (flight_id, departure_date_time, status, route_id, captain_pilot_id, first_officer_pilot_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (flight_id, departure, status, route_id, captain_id, officer_id))
        connection.commit()
        print(f"Great! Flight {flight_id} added successfully.")
    except Exception as e:
        print(f"Sorry. Failed to add flight: {e}")


def view_flights_by_criteria(cursor):
    print("\n<----- View Flights by Criteria ----->")
    print("1. By status")
    print("2. By route")
    print("3. By departure date")

    choice = input("Select criteria: ").strip()

    if choice == "1":
        status_choice = boolean_input("Select status (1 = Scheduled, 2 = Delayed, but use 3 for Cancelled): ", "1/2")
        # We need a slightly different approach here since there are 3 options
        # Let's handle status separately
        pass

    if choice == "1":
        print("1 = Scheduled, 2 = Delayed, 3 = Cancelled")
        raw = input("Select: ").strip()
        status_map = {"1": "Scheduled", "2": "Delayed", "3": "Cancelled"}
        status = status_map.get(raw)
        if not status:
            print("Invalid choice.")
            return
        cursor.execute("""
            SELECT f.flight_id, f.departure_date_time, f.status,
                   f.route_id, f.captain_pilot_id, f.first_officer_pilot_id
            FROM Flight f
            WHERE f.status = ?
            ORDER BY f.departure_date_time
        """, (status,))

    elif choice == "2":
        route_id = conformed_id_input("Route ID (e.g., CX001): ", r"^[A-Z]{2}[0-9]{3}$", "e.g., CX001")
        cursor.execute("""
            SELECT f.flight_id, f.departure_date_time, f.status,
                   f.route_id, f.captain_pilot_id, f.first_officer_pilot_id
            FROM Flight f
            WHERE f.route_id = ?
            ORDER BY f.departure_date_time
        """, (route_id,))

    elif choice == "3":
        date_input = non_empty_input("Enter date (YYYY-MM-DD): ")
        cursor.execute("""
            SELECT f.flight_id, f.departure_date_time, f.status,
                   f.route_id, f.captain_pilot_id, f.first_officer_pilot_id
            FROM Flight f
            WHERE f.departure_date_time LIKE ?
            ORDER BY f.departure_date_time
        """, (date_input + "%",))

    else:
        print("Invalid option.")
        return

    rows = cursor.fetchall()
    if not rows:
        print("No flights found for the selected criteria.")
        return

    for row in rows:
        print(row)


def update_flight_information(connection, cursor):
    print("\n<----- Update Flight Information ----->")

    flight_id = conformed_id_input("Flight ID to update (e.g., F001): ", r"^[A-Z]{1}[0-9]{3}$", "e.g., F001")
    if not record_exists(cursor, "Flight", "flight_id", flight_id):
        print(f"Sorry. Flight {flight_id} not found.")
        return

    print("What do you want to update?")
    print("1. Status")
    print("2. Departure date and time")
    choice = input("Select: ").strip()

    if choice == "1":
        print("1 = Scheduled, 2 = Delayed, 3 = Cancelled")
        raw = input("Select new status: ").strip()
        status_map = {"1": "Scheduled", "2": "Delayed", "3": "Cancelled"}
        new_value = status_map.get(raw)
        if not new_value:
            print("Invalid choice.")
            return
        column = "status"

    elif choice == "2":
        new_value = non_empty_input("New departure date and time (YYYY-MM-DD HH:MM:SS): ")
        column = "departure_date_time"

    else:
        print("Invalid option.")
        return

    try:
        cursor.execute(f"""
            UPDATE Flight SET {column} = ? WHERE flight_id = ?
        """, (new_value, flight_id))
        connection.commit()
        print(f"Great! Flight {flight_id} updated successfully.")
    except Exception as e:
        print(f"Sorry. Failed to update: {e}")


def flight_summary_by_destination(cursor):
    print("\n<----- Flights by Destination ----->")
    cursor.execute("""
        SELECT a.city, a.country, COUNT(f.flight_id) AS total_flights
        FROM Flight f
        JOIN Route r ON f.route_id = r.route_id
        JOIN Airport a ON r.destination_airport_id = a.airport_id
        GROUP BY a.airport_id
        ORDER BY total_flights DESC
    """)
    rows = cursor.fetchall()
    if not rows:
        print("No data found.")
        return
    for row in rows:
        print(f"{row[0]}, {row[1]}: {row[2]} flight(s)")


def flight_summary_by_pilot(cursor):
    print("\n<----- Flights by Pilot ----->")
    cursor.execute("""
        SELECT p.pilot_id, p.first_name || ' ' || p.last_name AS name, p.rank,
               COUNT(f.flight_id) AS total_flights
        FROM Pilot p
        LEFT JOIN Flight f ON p.pilot_id = f.captain_pilot_id OR p.pilot_id = f.first_officer_pilot_id
        GROUP BY p.pilot_id
        ORDER BY total_flights DESC
    """)
    rows = cursor.fetchall()
    if not rows:
        print("No data found.")
        return
    for row in rows:
        print(f"{row[0]} | {row[1]} ({row[2]}): {row[3]} flight(s)")