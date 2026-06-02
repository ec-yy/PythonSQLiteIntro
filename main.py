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
    connection = sqlite3.connect('airline.db')
    cursor = connection.cursor()
    connection.execute('PRAGMA foreign_keys = ON')
    return connection, cursor

def establish_database(cursor):
    cursor.execute('''
        CREATE TABLE Airport (
            airportId TEXT PRIMARY KEY,
            airportName TEXT NOT NULL,
            country TEXT NOT NULL,
            city TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE Pilot (
            pilotId TEXT PRIMARY KEY,
            licenseId TEXT NOT NULL,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            rank TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE Route (
            routeId TEXT PRIMARY KEY,
            durationMinutes INTEGER NOT NULL,
            originAirportId TEXT NOT NULL,
            destinationAirportId TEXT NOT NULL,
            FOREIGN KEY (originAirportId) REFERENCES Airport(airportId),
            FOREIGN KEY (destinationAirportId) REFERENCES Airport(airportId)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Flight (
            flightId TEXT PRIMARY KEY,
            departureDateTime TEXT NOT NULL,
            status TEXT NOT NULL,
            routeId TEXT NOT NULL,
            captainPilotId TEXT NOT NULL,
            1stOfficerPilotId TEXT NOT NULL,
            FOREIGN KEY (routeId) REFERENCES Route(routeId),
            FOREIGN KEY (captainPilotId) REFERENCES Pilot(pilotId),       
            FOREIGN KEY (1stOfficerPilotId) REFERENCES Pilot(pilotId)
        )
    ''')

    default_airport_data = [
        ("HKG", "Hong Kong International Airport", "China", "Hong Kong"),
        ("LAX", "Los Angeles International Airport", "United States", "Los Angeles"),
        ("NRT", "Narita International Airport", "Japan", "Narita"),
        ("LHR", "Heathrow Airport", "United Kingdom", "London")        
    ]

    default_pilot_data = [
        ("P001", "PIL-12345", "John", "Doe", "Captain"),
        ("P002", "PIL-67890", "Jane", "Smith", "First Officer")
    ]

    default_route_data = [
        ("CX001", 120, "HKG", "LAX"),
        ("CX002", 180, "LAX", "NRT"),
        ("CX003", 90, "NRT", "LHR"),
        ("CX004", 150, "LHR", "HKG")
    ]

    default_flight_data = [
        ("F001", "2023-06-01 08:00:00", "Scheduled", "CX001", "P001", "P002"),
        ("F002", "2023-06-01 14:00:00", "Scheduled", "CX002", "P002", "P001")
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
        INSERT INTO Flight (flightId, departureDateTime, status, routeId, captainPilotId, 1stOfficerPilotId)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', default_flight_data)

def main():
    reset = reset_database()
    connection, cursor = connect_database()

    if reset:
        establish_database(cursor)
        print("A new database has been initialized with default data.")
        connection.commit()

    print("Database ready.")
    connection.close()

main()

