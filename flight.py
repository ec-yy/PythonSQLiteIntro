# flight.py
# Handles all flight-related operations:
#   - add_new_flight            → Menu 2.4 (Add new flight)
#   - view_flights_by_criteria  → Menu 3   (View flights by criteria)
#   - update_flight_information → Menu 4   (Update flight information)
#   - flight_summary_by_destination → Menu 8.1
#   - flight_summary_by_pilot       → Menu 8.2

from rule import non_empty_input, valid_id_input, valid_date_time_format, valid_choice, record_exists, menu_choice

# ── Constants ────────────────────────────────────────────────────────────────

STATUS = ["On Schedule", "Delayed", "Cancelled", "Departed", "Arrived"]

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
            print("Sorry. Input is invalid.. Please choose 1-5 only.")
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
        print(f"Sorry. Flight {flight_id} already exists in the table. Go to option 4 of main menu if you would like to update airport records.")
        return

    departure_date_time = valid_date_time_format("Enter departure datetime (YYYY-MM-DD HH:MM:SS): ")

    status = _prompt_status()

    route_id = valid_id_input("Enter Route ID: ", r"^[A-Z]{2}[0-9]{3}$", "e.g., CX001")
    if not record_exists(cursor, "Route", "route_id", route_id):
        print(f"Route {route_id} not found. Please add the route first.")
        return

    captain_id = valid_id_input("Enter Captain Pilot ID: ", r"^[A-Z]{1}[0-9]{3}$", "e.g., P001")
    if not record_exists(cursor, "Pilot", "pilot_id", captain_id):
        print(f"Captain {captain_id} not found. Please add the pilot first.")
        return

    first_officer_id = valid_id_input("Enter First Officer Pilot ID: ", r"^[A-Z]{1}[0-9]{3}$", "e.g., P001")
    if not record_exists(cursor, "Pilot", "pilot_id", first_officer_id):
        print(f"First Officer {first_officer_id} not found. Please add the pilot first.")
        return

    if captain_id == first_officer_id:
        print("Captain and First Officer cannot be the same pilot.")
        return

    try:
        cursor.execute("""
            INSERT INTO Flight
                (flight_id, departure_date_time, status, route_id, captain_pilot_id, first_officer_pilot_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (flight_id, departure, status, route_id, captain_id, first_officer_id))
        connection.commit()
        print(f"Flight {flight_id} added successfully.")
    except Exception as e:
        print("Database error when adding flight:", e)


def view_flights_by_criteria(cursor):
    """
    Display flights filtered by destination city, status, and/or departure date.
    All filters are optional — press Enter to skip any of them.
    """
    print("\n--- View Flights by Criteria ---")
    print("Leave a field blank to skip that filter.\n")

    destination = input("Destination city: ").strip()

    # Status filter — only show the menu if the user wants to filter by status
    use_status = input("Filter by status? (Y/N): ").strip().upper()
    status_filter = None
    if use_status == "Y":
        status_filter = _prompt_status()

    date = input("Departure date (YYYY-MM-DD, or blank to skip): ").strip()

    query = """
        SELECT f.flightId,
               f.departureDateTime,
               f.status,
               a1.city AS fromCity,
               a2.city   AS toCity
        FROM Flight f
        JOIN Route   r  ON f.routeId              = r.routeId
        JOIN Airport a1 ON r.originAirportId      = a1.airportId
        JOIN Airport a2 ON r.destinationAirportId = a2.airportId
        WHERE 1 = 1
    """
    params = []

    if destination:
        query += " AND a2.city LIKE ?"
        params.append(f"%{destination}%")

    if status_filter:
        query += " AND f.status = ?"
        params.append(status_filter)

    if date:
        query += " AND f.departureDateTime LIKE ?"
        params.append(f"{date}%")

    query += " ORDER BY f.departureDateTime"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    if not rows:
        print("\nNo flights found for these criteria.")
        return

    print("\n{:<10} {:<22} {:<12} {:<12} {}".format(
        "Flight", "Departure", "Status", "From", "To"))
    print("-" * 65)
    for row in rows:
        print("{:<10} {:<22} {:<12} {:<12} {}".format(
            row[0], row[1], row[2], row[3], row[4]))


def update_flight_information(connection, cursor):
    """Update the departure datetime and/or status of an existing flight."""
    print("\n--- Update Flight Information ---")
    flight_id = require_non_empty("Enter Flight ID to update: ").upper()

    cursor.execute("""
        SELECT flightId, departureDateTime, status
        FROM Flight
        WHERE flightId = ?
    """, (flight_id,))
    row = cursor.fetchone()

    if not row:
        print(f"Flight {flight_id} not found.")
        return

    print(f"\nCurrent record:")
    print(f"  Flight ID  : {row[0]}")
    print(f"  Departure  : {row[1]}")
    print(f"  Status     : {row[2]}")
    print("\nPress Enter to keep the current value.")

    new_departure = input(f"New departure datetime [{row[1]}]: ").strip()
    updated_departure = new_departure if new_departure else row[1]

    # Reuse _prompt_status with current value so Enter keeps it unchanged
    updated_status = _prompt_status(current=row[2])

    try:
        cursor.execute("""
            UPDATE Flight
            SET departureDateTime = ?, status = ?
            WHERE flightId = ?
        """, (updated_departure, updated_status, flight_id))
        connection.commit()
        print("Flight updated successfully.")
    except Exception as e:
        print("Database error when updating flight:", e)


def flight_summary_by_destination(cursor):
    """
    Aggregate report: total number of flights grouped by destination city.
    Maps to Menu 8.1.
    """
    print("\n--- Number of Flights to Each Destination ---")
    cursor.execute("""
        SELECT a.city,
               a.country,
               COUNT(*) AS flightCount
        FROM Flight f
        JOIN Route   r ON f.routeId              = r.routeId
        JOIN Airport a ON r.destinationAirportId = a.airportId
        GROUP BY a.airportId
        ORDER BY flightCount DESC
    """)
    rows = cursor.fetchall()

    if not rows:
        print("No flight data available.")
        return

    print("\n{:<22} {:<18} {}".format("Destination City", "Country", "Flights"))
    print("-" * 50)
    for row in rows:
        print("{:<22} {:<18} {}".format(row[0], row[1], row[2]))


def flight_summary_by_pilot(cursor):
    """
    Aggregate report: total number of flights assigned to each pilot.
    Counts flights where the pilot appears as either Captain or First Officer.
    Maps to Menu 8.2.
    """
    print("\n--- Number of Flights Assigned to Each Pilot ---")
    cursor.execute("""
        SELECT p.pilotId,
               p.firstName || ' ' || p.lastName AS fullName,
               p.rank,
               COUNT(*) AS flightCount
        FROM Pilot p
        JOIN Flight f
          ON p.pilotId = f.captainPilotId
          OR p.pilotId = f.firstOfficerPilotId
        GROUP BY p.pilotId
        ORDER BY flightCount DESC
    """)
    rows = cursor.fetchall()

    if not rows:
        print("No pilot assignment data available.")
        return

    print("\n{:<10} {:<28} {:<18} {}".format(
        "Pilot ID", "Name", "Rank", "Flights"))
    print("-" * 65)
    for row in rows:
        print("{:<10} {:<28} {:<18} {}".format(
            row[0], row[1], row[2], row[3]))