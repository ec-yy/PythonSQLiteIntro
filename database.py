import sqlite3
import os

def reset_database():
    if os.path.exists('airline.db'):
        while True:
            choice = input("The system detects an existing database. Do you wish to reset it? (Y/N): ").strip().upper()
            if choice == 'Y':
                os.remove('airline.db')
                print("A new database will be created to override the existing database.")
                return True
            elif choice == 'N':
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
        raise

def establish_database(cursor):
    try:        
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Airport (
                    airportId TEXT PRIMARY KEY,
                    airportName TEXT NOT NULL,
                    country TEXT NOT NULL,
                    city TEXT NOT NULL
                )
            ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Pilot (
                    pilotId TEXT PRIMARY KEY,
                    licenseId TEXT NOT NULL,
                    firstName TEXT NOT NULL,
                    lastName TEXT NOT NULL,
                    rank TEXT NOT NULL
                )
            ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Route (
                    routeId TEXT PRIMARY KEY,
                    durationMinutes INTEGER NOT NULL,
                    originAirportId TEXT NOT NULL,
                    destinationAirportId TEXT NOT NULL,
                    FOREIGN KEY (originAirportId) REFERENCES Airport(airportId),
                    FOREIGN KEY (destinationAirportId) REFERENCES Airport(airportId)
                )
            ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Flight (
                    flightId TEXT PRIMARY KEY,
                    departureDateTime TEXT NOT NULL,
                    status TEXT NOT NULL,
                    routeId TEXT NOT NULL,
                    captainPilotId TEXT NOT NULL,
                    firstOfficerPilotId TEXT NOT NULL,
                    FOREIGN KEY (routeId) REFERENCES Route(routeId),
                    FOREIGN KEY (captainPilotId) REFERENCES Pilot(pilotId),       
                    FOREIGN KEY (firstOfficerPilotId) REFERENCES Pilot(pilotId)
                )
            ''')

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

        cursor.executemany('''
            INSERT INTO Airport (airportId, airportName, country, city)
            VALUES (?, ?, ?, ?)
        ''', default_airport_data)

        cursor.executemany('''
            INSERT INTO Pilot (pilotId, licenseId, firstName, lastName, rank)
            VALUES (?, ?, ?, ?, ?)
        ''', default_pilot_data)

        cursor.executemany('''
            INSERT INTO Route (routeId, durationMinutes, originAirportId, destinationAirportId)
            VALUES (?, ?, ?, ?)
        ''', default_route_data)

        cursor.executemany('''
            INSERT INTO Flight (flightId, departureDateTime, status, routeId, captainPilotId, firstOfficerPilotId)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', default_flight_data)
    
    except sqlite3.Error as e:
        print(f"An error occured when establishing the database: {e}")
        raise