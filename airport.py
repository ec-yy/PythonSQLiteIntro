from rule import non_empty_input, boolean_input, conformed_id_input, record_exists

# Function to add a new airport
def add_new_airport(connection, cursor):
    print("\n<--- Add a New Airport --->")

    #Provide an airport ID that conforms to a prescribed format (i.e., 3 uppercase letters)
    airport_id = conformed_id_input("Please provide airport ID (e.g. NRT): ", r"^[A-Z]{3}$", "e.g., NRT")

    if record_exists(cursor, "Airport", "airport_id", airport_id):
        print(f"Sorry. Airport {airport_id} exists in the table. Go to option 7 of main menu if you would like to update airport records.")
        return

    # Provide an airport name, country and city. All of them must be non-empty strings
    airport_name = non_empty_input("Airport name: ")
    country = non_empty_input("Country: ")
    city = non_empty_input("City: ")

    # Try to add a new airport to the table Airport based on user input and catch any exception
    try:
        cursor.execute(
            """
            INSERT INTO Airport (airport_id, airport_name, country, city)
            VALUES (?, ?, ?, ?)
            """,
            (airport_id, airport_name, country, city),
        )
        connection.commit()
        print(f"Airport {airport_id} is successfully added to the table Airport.")
    except Exception as e:
        print("Failure in addition of airport: ", e)


#Function to view or update specific airport information
def view_update_airport(connection, cursor):
    print("\n<--- View or Update Airport --->")

    # Provide an airport ID that conforms to a prescribed format (i.e., 3 uppercase letters)
    airport_id = conformed_id_input("Please provide airport ID (e.g. NRT): ", r"^[A-Z]{3}$", "e.g., NRT")

    # Try to fetch the airport record based on airport ID provided by user.
    cursor.execute(
        """
        SELECT *
        FROM Airport
        WHERE airport_id = ?
        """,
        (airport_id,),
    )
    row = cursor.fetchone()

    if not row:
        print(f"Airport {airport_id} is not found from the table Airport.")
        return

    print(f"\nAirport {airport_id}:")
    print(f"   Name    : {row[1]}")
    print(f"   Country : {row[2]}")
    print(f"   City    : {row[3]}")

    # Prompt user if they want to update the airport information.
    user_input = boolean_input("Do you want to update the information of this Airport record? (Y/N): ")
    if user_input == 'N':
        return

    print("\nSimply press enter to skip the current field and keep the current value.")
    revised_name = input(f"New airport name [{row[1]}]: ").strip()
    revised_country = input(f"New country [{row[2]}]: ").strip()
    revised_city = input(f"New city [{row[3]}]: ").strip()

    updated_name = revised_name if revised_name else row[1]
    updated_country = revised_country if revised_country else row[2]
    updated_city = revised_city if revised_city else row[3]

    # Try to update the airport record based on user input and catch any exception.
    try:
        cursor.execute(
            """
            UPDATE Airport
            SET airport_name = ?, country = ?, city = ?
            WHERE airport_id = ?
            """,
            (updated_name, updated_country, updated_city, airport_id),
        )
        connection.commit()
        print("Airport updated successfully.")
    except Exception as e:
        print("Database error when updating airport:", e)