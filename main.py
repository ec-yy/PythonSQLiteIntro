from database import connect_database, reset_database, establish_database

def main():
    reset = reset_database()
    connection, cursor = connect_database()

    if reset:
        establish_database(cursor)
        connection.commit()
        print("A new database has been initialized with default data.")
        
    print("Database ready.")
    connection.close()

main()

