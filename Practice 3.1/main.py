import sqlite3
conn = sqlite3.connect('store')



conn.execute("UPDATE pet SET name = 'Fluffyyyyyy' where owner = 'Harold'")

conn.commit()
print("Item updated successfully.")