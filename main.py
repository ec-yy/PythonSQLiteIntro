import sqlite3
from database import connect_database, reset_database, establish_database

def main():
    connection = None # To avoid scenario where "finally" block attempts to close a connection that does not exist
    
    try:
        reset = reset_database()
        connection, cursor = connect_database()

        if reset:
            establish_database(cursor)
            connection.commit()
            print("A new database has been initialized with default data.")
            
        print("Database ready.")
        
    except sqlite3.Error as e:
         print(f"Application halted due to an error: {e}")   

    finally: 
        try:
            if connection is not None:
                connection.close()

        except:
            pass

main()

