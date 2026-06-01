import sqlite3
import os

def run_program():
    if os.path.exists('airline.db'):
        while True:
            choice = input("The system detects an existing database. Do you wish to reset it? (Y/N): ").strip().upper()
            if choice == 'Y':
                os.remove('airline.db')
                print("A new database will be created to override the existing one.")
                connection, cursor = connect_database()
                try:
                    create_tables(connection, cursor)
                    insert_sample_data(connection, cursor)
                finally:
                    connection.close()
                break
            elif choice == 'N':
                print("The system will continue to use the existing database.")
                break
            else:
                print("Your input is not valid. Please input 'Y' or 'N'.")
    else:
        print("There is no existing database. The system will create a new database.")
        connection, cursor = connect_database()
        try:
            create_tables(connection, cursor)
            insert_sample_data(connection, cursor)
        finally:
            connection.close()

def connect_database():
    connection = sqlite3.connect('airline.db')
    cursor = connection.cursor()
    return connection, cursor

def create_tables(connection, cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Airport (
            airportId TEXT PRIMARY KEY,
            airportName TEXT NOT NULL,
            country TEXT NOT NULL,
            city TEXT NOT NULL
        )
    ''')
    connection.commit()

def insert_sample_data(connection, cursor):
    cursor.executemany('''
    INSERT INTO Airport (airportId, airportName, country, city)
    VALUES (?, ?, ?, ?)
    ''', [
        ("HKG", "Hong Kong International Airport", "China", "Hong Kong"),
        ("LAX", "Los Angeles International Airport", "United States", "Los Angeles"),
        ("NRT", "Narita International Airport", "Japan", "Narita"),
        ("LHR", "Heathrow Airport", "United Kingdom", "London")
    ])
    connection.commit()
 
run_program()


