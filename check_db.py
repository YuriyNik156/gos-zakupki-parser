import sqlite3

conn = sqlite3.connect("purchases.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM purchases")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
