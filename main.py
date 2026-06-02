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

    default_data = [
        ("HKG", "Hong Kong International Airport", "China", "Hong Kong"),
        ("LAX", "Los Angeles International Airport", "United States", "Los Angeles"),
        ("NRT", "Narita International Airport", "Japan", "Narita"),
        ("LHR", "Heathrow Airport", "United Kingdom", "London")        
    ]

    cursor.executemany('''
        INSERT INTO Airport (airportId, airportName, country, city)
        VALUES (?, ?, ?, ?)
    ''', default_data)

def main():
    reset = reset_database()
    connection, cursor = connect_database()

    if reset:
        establish_database(cursor)
        connection.commit()
        print("A new database has been initialized with default data.")
    
    connection.close()

main()

