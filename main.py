import sqlite3
from database import connect_database, reset_database, establish_database
from rule import view_table
from airport import add_new_airport, view_update_airport
from route import add_new_route


def menu_main():
    print("\n\n<=== Flight Management Appplication Main Menu ===>")
    print("1. All: View")
    print("2. All: Add")
    print("3. Flight: View flights by criteria")
    print("4. Flight: Update flight information")
    print("5. Pilot: Assign pilot to flight")
    print("6. Pilot: View pilot schedule")
    print("7. Airport: View or update airport information")
    print("8. All: Summary reports")
    print("0. Exit")

def sub_menu_view():
    print("\n\n<--- Sub Menu: View --->")
    print("1. View all airports")
    print("2. View all routes")
    print("3. View all pilots")
    print("4. View all flights")
    print("0. Back")

def sub_menu_add():
    print("\n\n<--- Sub Menu: Add --->")
    print("1. Add a new airport")
    print("2. Add a new route")
    print("3. Add a new pilot")
    print("4. Add a new flight")
    print("0. Back")

def sub_menu_summary():
    print("\n<--- Sub Menu: Summary Reports --->    ")
    print("1. Number of flights to each destination")
    print("2. Number of flights assigned to each pilot")
    print("0. Back")

def navigate_menu(connection, cursor):
    while True:
        menu_main()
        choice = input("Select an option: ").strip()

        if choice == "1":
            while True:
                sub_menu_view()
                sub_choice = input("Select an option: ").strip()
                if sub_choice == "1":
                    view_table(cursor, "Airport", order_by="airportId")
                elif sub_choice == "2":
                    view_table(cursor, "Route", order_by="routeId")
                elif sub_choice == "3":
                    view_table(cursor, "Pilot", order_by="pilotId")
                elif sub_choice == "4":
                    view_table(cursor, "Flight", order_by="departureDateTime")
                elif sub_choice == "0":
                    break
                else:
                    print("Invalid option. Please try again.")

        elif choice == "2":
            while True:
                sub_menu_add()
                sub_choice = input("Select an option: ").strip()
                if sub_choice == "1":
                    add_new_airport(connection, cursor)
                elif sub_choice == "2":
                    add_new_route(connection, cursor)
                elif sub_choice == "3":
                    add_new_pilot(connection, cursor)
                elif sub_choice == "4":
                    add_new_flight(connection, cursor)
                elif sub_choice == "0":
                    break
                else:
                    print("Invalid option. Please try again.")

        elif choice == "3":
            view_flights_by_criteria(cursor)

        elif choice == "4":
            update_flight_information(connection, cursor)

        elif choice == "5":
            assign_pilot_to_flight(connection, cursor)

        elif choice == "6":
            view_pilot_schedule(cursor)

        elif choice == "7":
            view_update_airport(connection, cursor)

        elif choice == "8":
            while True:
                sub_menu_summary()
                sub_choice = input("Select an option: ").strip()
                if sub_choice == "1":
                    flight_summary_by_destination(cursor)
                elif sub_choice == "2":
                    flight_summary_by_pilot(cursor)
                elif sub_choice == "0":
                    break
                else:
                    print("Invalid option. Please try again.")

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Please try again.")

def main():
    connection = None #To avoid scenario where "finally" block attempts to close a connection that does not exist
    
    try:
        reset = reset_database()
        connection, cursor = connect_database()

        if reset:
            establish_database(cursor)
            connection.commit()
            print("A new database has been initialized with default data.")
            
        print("Database ready.")
        navigate_menu(connection, cursor)
        
    except sqlite3.Error as e:
         print(f"Application aborted due to an error: {e}")   

    finally: 
        try:
            if connection is not None:
                connection.close()

        except:
            pass


if __name__ == "__main__":
    main()

