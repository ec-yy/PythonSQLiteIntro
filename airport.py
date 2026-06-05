from rule import non_empty_input, boolean_input, record_exists


def add_new_airport(connection, cursor):
    print("\n<--- Add a New Airport --->")
    airport_id = non_empty_input("Please provide airport ID (e.g. NRT): ").upper()

    if record_exists(cursor, "Airport", "airport_id", airport_id):
        print(f"Sorry. Airport {airport_id} exists in the table. Go to option 7 of main menu if you would like to update airport records.")
        return

    airport_name = non_empty_input("Airport name: ")
    country = non_empty_input("Country: ")
    city = non_empty_input("City: ")

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


def view_update_airport(connection, cursor):
    print("\n<--- View or Update Airport --->")
    airport_id = non_empty_input("Enter airport ID (e.g., NRT) to view/update: ").upper()

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

    user_input = boolean_input("Do you want to update the information of this Airport record? (Y/N): ")
    if user_input == 'N':
        return

    print("\nSimply press enter to skip the current record and keep the current value.")
    revised_name = input(f"New airport name [{row[1]}]: ").strip()
    revised_country = input(f"New country [{row[2]}]: ").strip()
    revised_city = input(f"New city [{row[3]}]: ").strip()

    updated_name = revised_name if revised_name else row[1]
    updated_country = revised_country if revised_country else row[2]
    updated_city = revised_city if revised_city else row[3]

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