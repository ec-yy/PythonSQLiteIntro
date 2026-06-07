# This module contains functions to undertake flight-related operations, including:

# flight.py
# Handles all flight-related operations:
#   - add_new_flight            → Menu 2.4 (Add new flight)
#   - view_flights_by_criteria  → Menu 3   (View flights by criteria)
#   - update_flight_information → Menu 4   (Update flight information)
#   - flight_summary_by_destination → Menu 8.1
#   - flight_summary_by_pilot       → Menu 8.2

from rule import valid_id_input, valid_date_time_format, valid_date_format, valid_choice, valid_pilot_rank, record_exists

# ── Constants ────────────────────────────────────────────────────────────────

# Maps numeric menu choice → status string.
# Square-bracket access is safe here because menu_choice() guarantees
# the key will always be "1", "2", or "3".
STATUS_MAP = {"1": "On Schedule", "2": "Delayed", "3": "Cancelled", "4": "Departed", "5": "Arrived"}


# ── Helper ───────────────────────────────────────────────────────────────────

def _prompt_status(current=None):
    """
    Displays the status menu and returns the chosen status string.
    If `current` is provided, the user may press Enter to keep the current value.
    """
    print("\n<----- Flight Status ----->")
    print(" Select status: ")
    print("  1: On Schedule")
    print("  2: Delayed")
    print("  3: Cancelled")
    print("  4: Departed")
    print("  5: Arrived")

    if current:
        # Allow blank input to keep the existing value
        while True:
            raw_input = input(f"Please choose 1-5 [current: {current}] (Note: Press Enter to keep current): ").strip()
            if not raw_input:
                return current          # keep unchanged
            if raw_input in ("1", "2", "3", "4", "5"):
                return STATUS_MAP[raw_input]
            print("Sorry. Input is invalid. Please choose 1-5 only.")
    else:
        raw_input = valid_choice("Please choose 1-5: ", ["1", "2", "3", "4", "5"])
        return STATUS_MAP[raw_input]


# ── Core functions ────────────────────────────────────────────────────────────

# Function to add a new flight
def add_new_flight(connection, cursor):
    print("\n<----- Add a New Flight ----->")

    # Provide a flight ID that conforms to a prescribed format (i.e., 1 uppercase letter followed by 3 digits).
    flight_id = valid_id_input("Enter Flight ID (e.g. F001): ", r"^[A-Z][0-9]{3}$", "e.g., F001")

    if record_exists(cursor, "Flight", "flight_id", flight_id):
        print(f"Sorry. Flight {flight_id} already exists in the table. Go to option 4 of main menu if you would like to update flight records.")
        return

    departure_date_time = valid_date_time_format("Enter departure datetime (YYYY-MM-DD HH:MM:SS): ", mandatory_input=True)

    status = _prompt_status()

    while True:
        route_id = valid_id_input("Enter Route ID: ", r"^[A-Z]{2}[0-9]{3}$", "e.g., CX001")
        if not record_exists(cursor, "Route", "route_id", route_id):
            print(f"Sorry. Route {route_id} is not found in the table Route. Please try again.")
            continue
        break

    while True:
        captain_id = valid_id_input("Enter Captain Pilot ID: ", r"^[A-Z][0-9]{3}$", "e.g., P001")
        if not record_exists(cursor, "Pilot", "pilot_id", captain_id):
            print(f"Sorry. Captain {captain_id} is not found in the table Pilot. Please try again.")
            continue
        if not valid_pilot_rank(cursor, captain_id, "Captain"):
            print(f"Sorry. Pilot {captain_id} does not hold the rank of Captain. Please try again.")
            continue
        break

    while True:
        first_officer_id = valid_id_input("Enter First Officer Pilot ID: ", r"^[A-Z][0-9]{3}$", "e.g., P001")
        if not record_exists(cursor, "Pilot", "pilot_id", first_officer_id):
            print(f"Sorry. First Officer {first_officer_id} is not found in the table Pilot. Please try again.")
            continue
        if not valid_pilot_rank(cursor, first_officer_id, "First Officer"):
            print(f"Sorry. Pilot {first_officer_id} does not hold the rank of First Officer. Please try again.")
            continue
        break

    try:
        cursor.execute("""
            INSERT INTO Flight
                (flight_id, departure_date_time, status, route_id, captain_pilot_id, first_officer_pilot_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (flight_id, departure_date_time, status, route_id, captain_id, first_officer_id))
        connection.commit()
        print(f"Great! Flight {flight_id} is successfully added to the table Flight.")
    except Exception as e:
        print("Sorry. Failure in addition of flight:", e)


# Function to view flights by user-defined criteria
def view_flights_by_criteria(cursor):
    """
    Display flights filtered by destination city, status, and/or departure date.
    All filters are optional — press Enter to skip any of them.
    """
    print("\n<----- View Flights by Criteria ----->")
    print("Please leave the field blank to skip the filter.\n")

    # Departure date filter — only require input of departure date if the user wants to filter by departure date
    # valid_choice is configured to ensure non-empty input
    departure_date = None
    if valid_choice("Do you want to apply filter by departure date? (Y/N): ", ["Y", "N"]) == "Y":
        departure_date = valid_date_format("Date of Departure (Input Format: YYYY-MM-DD): ")

    # Status filter — only show the menu if the user wants to filter by status
    filter_by_status = valid_choice("Do you want to apply filter by flight status? (Y/N): ", ["Y", "N"])
    status_filter = None
    if filter_by_status == "Y":
        status_filter = _prompt_status()

    destination_country = input("Destination country: ").strip()

    destination_city = input("Destination city: ").strip()

    query = """
        SELECT flight.flight_id,
               flight.departure_date_time,
               flight.status,
               origin_airport.country AS from_country,
               origin_airport.city AS from_city,
               destination_airport.country AS to_country,
               destination_airport.city AS to_city
        FROM Flight flight
        JOIN Route route ON flight.route_id = route.route_id
        JOIN Airport origin_airport ON route.origin_airport_id = origin_airport.airport_id
        JOIN Airport destination_airport ON route.destination_airport_id = destination_airport.airport_id
        WHERE 1 = 1
    """
    parameter = []

    if departure_date:
        query += " AND flight.departure_date_time LIKE ?"
        parameter.append(f"{departure_date}%")

    if status_filter:
        query += " AND flight.status = ?"
        parameter.append(status_filter)

    if destination_country:
        query += " AND destination_airport.country LIKE ?"
        parameter.append(f"%{destination_country}%")

    if destination_city:
        query += " AND destination_airport.city LIKE ?"
        parameter.append(f"%{destination_city}%")

    query += " ORDER BY flight.departure_date_time"

    cursor.execute(query, parameter)
    rows = cursor.fetchall()

    if not rows:
        print("\nSorry. No flights can be found for these criteria.")
        return

    print("\n{:<10} {:<22} {:<12} {:<12} {:<18} {:<12} {}".format(
        "Flight", "Departure Date and Time", "Status", "From Country", "From City", "To Country", "To City"))
    print("-" * 100)
    for row in rows:
        print("{:<10} {:<22} {:<12} {:<12} {:<18} {:<12} {}".format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

# Function to update flight information (departure datetime and status)
def update_flight_information(connection, cursor):
    """Update the departure datetime and/or status of an existing flight."""
    print("\n<----- Update Flight Information ----->")
    flight_id = valid_id_input("Enter Flight ID (e.g. F001): ", r"^[A-Z][0-9]{3}$", "e.g., F001")

    cursor.execute("""
        SELECT flight_id, departure_date_time, status
        FROM Flight
        WHERE flight_id = ?
    """, (flight_id,))
    row = cursor.fetchone()

    if not row:
        print(f"Sorry. Flight {flight_id} is not found in the table Flight.")
        return

    print(f"\nCurrent record:")
    print(f"  Flight ID                : {row[0]}")
    print(f"  Departure Date and Time  : {row[1]}")
    print(f"  Status                   : {row[2]}")

    # Prompt user if they want to update the flight information.
    user_input = valid_choice("Do you want to update the information of this Flight record? (Y/N): ", ["Y", "N"])
    if user_input == 'N':
        return

    print("\nSimply press enter to skip the current field and keep the current value.") 
    prompt = f"New departure date and time [{row[1]}] (Input Format: YYYY-MM-DD HH:MM:SS, or leave blank to skip): "
    raw_input = valid_date_time_format(prompt, mandatory_input=False)  # allow blank input to keep current value
    updated_departure_date_time = raw_input if raw_input else row[1]

    # Reuse _prompt_status with current value so Enter keeps it unchanged
    updated_status = _prompt_status(current=row[2])

    try:
        cursor.execute("""
            UPDATE Flight
            SET departure_date_time = ?, status = ?
            WHERE flight_id = ?
        """, (updated_departure_date_time, updated_status, flight_id))
        connection.commit()
        print(f"Great! Flight {flight_id} is updated successfully.")
    except Exception as e:
        print(f"Sorry. Database error when updating flight {flight_id}: {e}")


def flight_summary_by_destination(cursor):
    """
    Aggregate report: total number of flights grouped by destination city.
    Maps to Menu 8.1.
    """
    print("\n<----- Number of Flights by Destination ----->")
    cursor.execute("""
        SELECT airport.country,
               airport.city,
               COUNT(*) AS flight_count
        FROM Flight flight
        JOIN Route route ON flight.route_id = route.route_id
        JOIN Airport airport ON route.destination_airport_id = airport.airport_id
        GROUP BY airport.airport_id
        ORDER BY flight_count DESC
    """)
    rows = cursor.fetchall()

    if not rows:
        print("Sorry. No flight data is available.")
        return

    print("\n{:<18} {:<22} {}".format("Destination Country", "City", "No. of Flights"))
    print("-" * 50)
    for row in rows:
        print("{:<18} {:<22} {}".format(row[0], row[1], row[2]))


def flight_summary_by_pilot(cursor):
    """
    Aggregate report: total number of flights assigned to each pilot.
    Counts flights where the pilot appears as either Captain or First Officer.
    Maps to Menu 8.2.
    """
    print("\n<----- Flight Summary by Pilot ----->")
    cursor.execute("""
        SELECT pilot.pilot_id,
               pilot.first_name || ' ' || pilot.last_name AS full_name,
               pilot.rank,
               COUNT(*) AS flight_count
        FROM Pilot pilot
        JOIN Flight flight
          ON pilot.pilot_id = flight.captain_pilot_id
          OR pilot.pilot_id = flight.first_officer_pilot_id
        GROUP BY pilot.pilot_id
        ORDER BY flight_count DESC
    """)
    rows = cursor.fetchall()

    if not rows:
        print("Sorry. No pilot assignment data is available.")
        return

    print("\n{:<10} {:<28} {:<18} {}".format(
        "Pilot ID", "Full Name", "Rank", "Flights"))
    print("-" * 65)
    for row in rows:
        print("{:<10} {:<28} {:<18} {}".format(
            row[0], row[1], row[2], row[3]))