import sqlite3
import os
from rule import boolean_input 


def reset_database():
    if os.path.exists('airline.db'):
        user_input = boolean_input("The system detects an existing database. Do you wish to reset it? (Y/N): ", "Y/N")
        if user_input == 'Y':
            os.remove('airline.db')
            print("A new database will be created to override the existing database.")
            return True
        else:
            print("The system will continue to use the existing database.")
            return False
    else:
        return True


def connect_database():
    try:
        connection = sqlite3.connect('airline.db')
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')
        return connection, cursor
    except sqlite3.Error as e:
        print(f"An error occured when connecting to the database: {e}")
        # Ensure the error is raised to main() and caught the outer try-exception block there.
        raise


def establish_database(cursor):
    
    default_airport_data = [
        ("HKG", "Hong Kong International Airport", "Hong Kong", "Hong Kong"),
        ("NRT", "Narita International Airport", "Japan", "Tokyo"),
        ("LHR", "Heathrow Airport", "United Kingdom", "London"),
        ("SIN", "Changi Airport", "Singapore", "Singapore"),
        ("ICN", "Incheon International Airport", "South Korea", "Seoul"),
        ("BKK", "Suvarnabhumi Airport", "Thailand", "Bangkok"),
        ("SYD", "Sydney Airport", "Australia", "Sydney"),
        ("JFK", "John F. Kennedy International Airport", "USA", "New York"),
        ("LAX", "Los Angeles International Airport", "USA", "Los Angeles"),
        ("CDG", "Charles de Gaulle Airport", "France", "Paris")     
    ]

    default_pilot_data = [
        ("P001", "PLI001", "John", "Chan", "Captain"),
        ("P002", "PLI002", "Mary", "Lee", "First Officer"),
        ("P003", "PLI003", "Peter", "Wong", "Captain"),
        ("P004", "PLI004", "Alice", "Lam", "First Officer"),
        ("P005", "PLI005", "David", "Cheung", "Captain"),
        ("P006", "PLI006", "Sarah", "Ng", "First Officer"),
        ("P007", "PLI007", "Michael", "Ho", "Captain"),
        ("P008", "PLI008", "Emily", "Yip", "First Officer"),
        ("P009", "PLI009", "Chris", "Lau", "Captain"),
        ("P010", "PLI010", "Sophie", "Mak", "First Officer")
    ]

    default_route_data = [
        ("CX001", 300, "HKG", "NRT"),
        ("CX002", 840, "HKG", "LHR"),
        ("CX003", 240, "HKG", "SIN"),
        ("CX004", 210, "HKG", "ICN"),
        ("CX005", 180, "HKG", "BKK"),
        ("CX006", 540, "HKG", "SYD"),
        ("CX007", 900, "HKG", "JFK"),
        ("CX008", 780, "HKG", "LAX"),
        ("CX009", 780, "HKG", "CDG"),
        ("CX010", 240, "SIN", "BKK")
    ]

    default_flight_data = [
        ("F001", "2026-06-10 08:00:00", "Scheduled", "CX001", "P001", "P002"),
        ("F002", "2026-06-10 12:00:00", "Scheduled", "CX002", "P003", "P004"),
        ("F003", "2026-06-11 09:00:00", "Delayed", "CX003", "P005", "P006"),
        ("F004", "2026-06-11 14:30:00", "Scheduled", "CX004", "P007", "P008"),
        ("F005", "2026-06-12 07:15:00", "Cancelled", "CX005", "P009", "P010"),
        ("F006", "2026-06-12 16:00:00", "Scheduled", "CX006", "P001", "P004"),
        ("F007", "2026-06-13 10:45:00", "Scheduled", "CX007", "P003", "P006"),
        ("F008", "2026-06-13 20:00:00", "Delayed", "CX008", "P005", "P008"),
        ("F009", "2026-06-14 06:30:00", "Scheduled", "CX009", "P007", "P010"),
        ("F010", "2026-06-14 11:20:00", "Scheduled", "CX010", "P009", "P002")
        ]    
    
    
    try:        
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Airport (
                    airport_id TEXT PRIMARY KEY,
                    airport_name TEXT NOT NULL,
                    country TEXT NOT NULL,
                    city TEXT NOT NULL
                )
            ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Pilot (
                    pilot_id TEXT PRIMARY KEY,
                    license_id TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    rank TEXT NOT NULL
                )
            ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Route (
                    route_id TEXT PRIMARY KEY,
                    duration_minutes INTEGER NOT NULL,
                    origin_airport_id TEXT NOT NULL,
                    destination_airport_id TEXT NOT NULL,
                    FOREIGN KEY (origin_airport_id) REFERENCES Airport(airport_id),
                    FOREIGN KEY (destination_airport_id) REFERENCES Airport(airport_id)
                )
            ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Flight (
                    flight_id TEXT PRIMARY KEY,
                    departure_date_time TEXT NOT NULL,
                    status TEXT NOT NULL,
                    route_id TEXT NOT NULL,
                    captain_pilot_id TEXT NOT NULL,
                    first_officer_pilot_id TEXT NOT NULL,
                    FOREIGN KEY (route_id) REFERENCES Route(route_id),
                    FOREIGN KEY (captain_pilot_id) REFERENCES Pilot(pilot_id),
                    FOREIGN KEY (first_officer_pilot_id) REFERENCES Pilot(pilot_id)
                )
            ''')

        # Using executemany() to insert a list of multiple tuples of default data into each table.
        # Avoid using for loop and multiple calls of execution functions.
        cursor.executemany('''
            INSERT INTO Airport (airport_id, airport_name, country, city)
            VALUES (?, ?, ?, ?)
        ''', default_airport_data)

        cursor.executemany('''
            INSERT INTO Pilot (pilot_id, license_id, first_name, last_name, rank)
            VALUES (?, ?, ?, ?, ?)
        ''', default_pilot_data)

        cursor.executemany('''
            INSERT INTO Route (route_id, duration_minutes, origin_airport_id, destination_airport_id)
            VALUES (?, ?, ?, ?)
        ''', default_route_data)

        cursor.executemany('''
            INSERT INTO Flight (flight_id, departure_date_time, status, route_id, captain_pilot_id, first_officer_pilot_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', default_flight_data)
    
    except sqlite3.Error as e:
        print(f"An error occured when establishing the database: {e}")
        # Ensure the error is raised to main() and caught the outer try-exception block there.
        # Ensure connection.commit() is never called.
        raise