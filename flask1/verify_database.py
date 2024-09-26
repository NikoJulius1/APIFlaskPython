import sqlite3

# Forbind til database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Tjek om table findes og tæl antallet af records
c.execute("SELECT COUNT(*) FROM members")
count = c.fetchone()[0]
print(f"Number of records in the members table: {count}")

# Hvis de eksisterer, fetch og print dem
if count > 0:
    c.execute("SELECT * FROM members")
    members = c.fetchall()

    for member in members:
        print(member)

# Luk forbindelsen
conn.close()
