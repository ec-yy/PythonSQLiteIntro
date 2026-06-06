from rule import positive_integer_input, valid_id_input, record_exists


# Function to add a new route.  
def add_new_route(connection, cursor):
    print("\n<--- Add New Route --->")
    
    # Provide a route ID that conforms to a prescribed format (i.e., 2 uppercase letters followed by 3 digits).
    route_id = valid_id_input("Please provide Route ID (e.g. CX001): ", r"^[A-Z]{2}[0-9]{3}$", "e.g., CX001")
    if record_exists(cursor, "Route", "route_id", route_id):
        print(f"Sorry. Route {route_id} already exists in the table.")
        return

    # Provide a duration (measured in minutes) that is a positive integer.
    duration = positive_integer_input("Please provide duration (in minutes): ")

    # Provide origin and destination airports
    # They both conform to a prescribed format (i.e., 3 uppercase letters) and are different.
    origin, destination = None, None

    while True:
        if origin is None:
            origin_input = valid_id_input("Enter Origin Airport ID (e.g., NRF): ", r"^[A-Z]{3}$", "e.g., NRT")
            if not record_exists(cursor, "Airport", "airport_id", origin_input):
                print(f"Sorry. Origin airport {origin_input} not found. Please try again.")
                continue
            origin = origin_input

        if destination is None:
            destination_input = valid_id_input("Enter Destination Airport ID (e.g., NRF): ", r"^[A-Z]{3}$", "e.g., NRT")
            if not record_exists(cursor, "Airport", "airport_id", destination_input):
                print(f"Sorry.Destination airport {destination_input} not found. Please try again.")
                continue
            destination = destination_input

        if origin == destination:
            print("Sorry. Origin and destination cannot be the same airport.")
            destination = None
            continue

        break

    print(f"Great! Origin and destination are validated. The route from {origin} to {destination} will be adopted.")

    # Try to add a new route to the table Route based on user input and catch any exception.
    try:
        cursor.execute("""
            INSERT INTO Route (route_id, duration_minutes, origin_airport_id, destination_airport_id)
            VALUES (?, ?, ?, ?)
        """, (route_id, duration, origin, destination))
        connection.commit()
        print(f"Great! Route {route_id} added successfully.")
    
    except Exception as e:
        print("Sorry. Failure in addition of route: ", e)